from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from orders.models import Order
from users.forms import CustomUserCreationForm
from orders.forms import OrderStatusForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Вы успешно зарегистировались, теперь войдите в аккаунт!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = reverse_lazy('login')

    def get_template_names(self):
        user = self.request.user
        if user.places.exists():
            return ['users/profile_owner.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.places.exists():
            places = user.places.all()
            orders = Order.objects.filter(place__in=places).order_by('-created_at')[:10]
            context.update({
                'places': places,
                'orders': orders,
                # Добавь сюда статистику, если нужно
            })
        else:
            orders = Order.objects.filter(user=user).order_by('-created_at')[:10]
            context.update({
                'orders': orders,
            })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum
import json

class ManagerProfileView(TemplateView):
    template_name = 'users/manager_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = getattr(self.request.user, 'managed_address', None)
        context['address'] = address

        if address:
            places = address.places.all()
            orders = Order.objects.filter(place__in=places).order_by('-created_at')
            context['order_forms'] = [
                (order, OrderStatusForm(instance=order, prefix=f'order_{order.id}'))
                for order in orders
            ]

            # Подготовим данные для графиков
            def generate_period_data(days_back, interval):
                base = now()
                result = []
                for i in range(days_back):
                    if interval == 'day':
                        start = base - timedelta(days=i + 1)
                        end = base - timedelta(days=i)
                        label = start.strftime('%d.%m')
                    elif interval == 'week':
                        start = base - timedelta(weeks=i + 1)
                        end = base - timedelta(weeks=i)
                        label = f"Неделя {end.strftime('%W')}"
                    elif interval == 'month':
                        end = (base.replace(day=1) - timedelta(days=1)).replace(day=1)
                        start = (end - timedelta(days=30 * i)).replace(day=1)
                        label = start.strftime('%b %Y')
                    else:
                        continue

                    total = orders.filter(created_at__gte=start, created_at__lt=end).aggregate(
                        revenue=Sum('total_price')
                    )['revenue'] or 0

                    # Преобразуем Decimal в float перед сериализацией в JSON
                    result.append({'label': label, 'revenue': float(total)})

                return list(reversed(result))

            import json

            context['chart_data'] = json.dumps({
                'day': generate_period_data(7, 'day'),
                'week': generate_period_data(4, 'week'),
                'month': generate_period_data(6, 'month'),
            }, default=str)  # Это гарантирует корректную сериализацию Decimal в строки

        else:
            context['order_forms'] = []

        return context
