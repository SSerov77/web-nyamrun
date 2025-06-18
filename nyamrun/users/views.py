from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncDate, TruncHour
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import now, timedelta
from django.views import View
from django.views.generic import TemplateView
from orders.models import Order, OrderStatus
from users.forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Вы успешно зарегистировались, теперь войдите в аккаунт!"
            )
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/signup.html", {"form": form})


class ProfileView(LoginRequiredMixin, View):
    """Главное представление профиля с автоматическим перенаправлением"""
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Проверяем права доступа и перенаправляем соответственно
        
        # 1. Проверяем, является ли пользователь администратором
        if user.is_staff or user.is_superuser:
            return redirect('/admin/')
        
        # 2. Проверяем, является ли пользователь владельцем заведения
        elif user.places.exists():
            return redirect('owner_profile')
        
        # 3. Проверяем, является ли пользователь менеджером
        elif hasattr(user, 'managed_address') and user.managed_address:
            return redirect('manager_profile')
        
        # 4. Обычный пользователь
        else:
            return redirect('user_profile')


class OwnerProfileView(LoginRequiredMixin, TemplateView):
    """Личный кабинет владельца заведения"""
    template_name = "users/profile_owner.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Проверяем, что пользователь действительно владелец
        if not user.places.exists():
            return redirect('profile')

        # Период — день/неделя/месяц
        period = self.request.GET.get("period", "week")
        if period == "day":
            date_from = now() - timedelta(days=1)
        elif period == "month":
            date_from = now() - timedelta(days=30)
        else:
            date_from = now() - timedelta(days=7)

        context["selected_period"] = period

        places = user.places.all()
        selected_place_id = self.request.GET.get("place")
        selected_place = (
            places.filter(id=selected_place_id).first()
            if selected_place_id
            else places.first()
        )

        orders = Order.objects.filter(
            place=selected_place, created_at__gte=date_from
        )

        context.update(
            {
                "places": places,
                "selected_place": selected_place,
                "stats": self.get_statistics(orders),
                "address_stats": self.get_address_stats(selected_place, date_from),
            }
        )

        return context

    def get_statistics(self, orders):
        stats = {
            "total_orders": orders.count(),
            "total_revenue": orders.aggregate(Sum("total_price"))["total_price__sum"]
            or 0,
            "average_check": orders.aggregate(Avg("total_price"))["total_price__avg"]
            or 0,
        }

        status_counts = orders.values("status").annotate(count=Count("id"))
        stats["status_breakdown"] = [
            {
                "status": dict(OrderStatus.choices).get(s["status"], s["status"]),
                "count": s["count"],
            }
            for s in status_counts
        ]

        period = self.request.GET.get("period", "week")

        if period == "day":
            time_group = TruncHour("created_at")
            time_format = "%H:%M"
        else:
            time_group = TruncDate("created_at")
            time_format = "%d.%m"

        grouped_orders = (
            orders.annotate(time_key=time_group)
            .values("time_key")
            .annotate(total=Count("id"))
            .order_by("time_key")
        )

        stats["orders_chart"] = [
            {"label": o["time_key"].strftime(time_format), "value": o["total"]}
            for o in grouped_orders
        ]

        return stats

    def get_address_stats(self, place, date_from):
        result = []
        for addr in place.addresses.all():
            addr_orders = Order.objects.filter(
                place=place, address=addr, created_at__gte=date_from
            )
            result.append(
                {
                    "address": addr,
                    "total_orders": addr_orders.count(),
                    "total_revenue": addr_orders.aggregate(Sum("total_price"))[
                        "total_price__sum"
                    ]
                    or 0,
                    "average_check": addr_orders.aggregate(Avg("total_price"))[
                        "total_price__avg"
                    ]
                    or 0,
                }
            )
        return result


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Личный кабинет обычного пользователя"""
    template_name = "users/profile.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Показываем последние заказы пользователя
        orders = Order.objects.filter(user=user).order_by("-created_at")[:10]
        context["orders"] = orders

        return context


class ManagerProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        address = getattr(user, "managed_address", None)

        if not address:
            context["error"] = "Вы не привязаны к адресу"
            return context

        today = now().date()
        tomorrow = today + timedelta(days=1)

        orders = Order.objects.filter(address=address).prefetch_related(
            "items__product", "items__options", "user"
        )
        today_orders = orders.filter(created_at__date=today)
        upcoming_orders = orders.filter(
            created_at__date__in=[today, tomorrow]
        ).order_by("-created_at")
        issued_orders_count = orders.filter(status="issued").count()

        # Графи
        chart_data = (
            today_orders.annotate(hour=TruncHour("created_at"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )
        orders_chart = [
            {"label": item["hour"].strftime("%H:%M"), "value": item["count"]}
            for item in chart_data
        ]

        # Среднее время приготовления (ручной расчёт)
        ready_times = [o.ready_time for o in today_orders if o.ready_time]
        if ready_times:
            total_seconds = sum(
                [t.hour * 3600 + t.minute * 60 + t.second for t in ready_times]
            )
            avg_seconds = total_seconds // len(ready_times)
            average_ready_time = timedelta(seconds=avg_seconds)
        else:
            average_ready_time = None

        context.update(
            {
                "address": address,
                "orders_today": today_orders.count(),
                "orders_ready": today_orders.filter(status="ready").count(),
                "orders_created": today_orders.filter(status="created").count(),
                "orders_canceled": today_orders.filter(status="canceled").count(),
                "orders_chart": orders_chart,
                "average_ready_time": average_ready_time,
                "orders": upcoming_orders,
                "order_status_choices": OrderStatus.choices,
                "total_issued_orders": issued_orders_count,
            }
        )
        return context


class ManagerOrderStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        user = request.user
        address = getattr(user, "managed_address", None)
        order = get_object_or_404(Order, id=order_id, address=address)

        new_status = request.POST.get("status")
        if new_status in OrderStatus.values:
            order.status = new_status
            order.save(update_fields=["status"])
        return redirect("manager_profile")


def privacy_policy(request):
    return render(request, "users/privacy_policy.html")


def cookie_usage_policy(request):
    return render(request, "users/cookie_usage_policy.html")


def terms_of_use(request):
    return render(request, "users/terms_of_use.html")
