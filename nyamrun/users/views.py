from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from orders.models import Order
from users.forms import CustomUserCreationForm
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Sum, Avg, Count
from django.utils.timezone import now, timedelta
from django.db.models.functions import TruncHour, TruncDate

from places.models import Place, Address
from orders.models import Order, OrderStatus


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

        # Период — день/неделя/месяц
        period = self.request.GET.get('period', 'week')
        if period == 'day':
            date_from = now() - timedelta(days=1)
        elif period == 'month':
            date_from = now() - timedelta(days=30)
        else:
            date_from = now() - timedelta(days=7)

        context['selected_period'] = period

        if user.places.exists():
            places = user.places.all()
            selected_place_id = self.request.GET.get('place')
            selected_place = places.filter(id=selected_place_id).first() if selected_place_id else places.first()

            all_orders = Order.objects.filter(place__in=places)
            orders = Order.objects.filter(place=selected_place, created_at__gte=date_from)

            context.update({
                'places': places,
                'selected_place': selected_place,
                'stats': self.get_statistics(orders),
                'address_stats': self.get_address_stats(selected_place, date_from),
            })
        else:
            orders = Order.objects.filter(user=user).order_by('-created_at')[:10]
            context['orders'] = orders

        return context

    def get_statistics(self, orders):
        stats = {
            'total_orders': orders.count(),
            'total_revenue': orders.aggregate(Sum('total_price'))['total_price__sum'] or 0,
            'average_check': orders.aggregate(Avg('total_price'))['total_price__avg'] or 0,
        }

        status_counts = orders.values('status').annotate(count=Count('id'))
        stats['status_breakdown'] = [
            {
                'status': dict(OrderStatus.choices).get(s['status'], s['status']),
                'count': s['count']
            }
            for s in status_counts
        ]

        period = self.request.GET.get('period', 'week')

        if period == 'day':
            time_group = TruncHour('created_at')
            time_format = '%H:%M'
        else:
            time_group = TruncDate('created_at')
            time_format = '%d.%m'

        grouped_orders = (
            orders.annotate(time_key=time_group)
                .values('time_key')
                .annotate(total=Count('id'))
                .order_by('time_key')
        )

        stats['orders_chart'] = [
            {'label': o['time_key'].strftime(time_format), 'value': o['total']}
            for o in grouped_orders
        ]

        return stats

    def get_address_stats(self, place, date_from):
        result = []
        for addr in place.addresses.all():
            addr_orders = Order.objects.filter(place=place, address=addr, created_at__gte=date_from)
            result.append({
                'address': addr,
                'total_orders': addr_orders.count(),
                'total_revenue': addr_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0,
                'average_check': addr_orders.aggregate(Avg('total_price'))['total_price__avg'] or 0,
            })
        return result

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    

class ManagerProfileView(TemplateView):
    template_name = 'users/manager_profile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         address = getattr(self.request.user, 'managed_address', None)
#         context['address'] = address

#         if address:
#             places = address.places.all()
#             orders = Order.objects.filter(place__in=places).order_by('-created_at')
#             context['order_forms'] = [
#                 (order, OrderStatusForm(instance=order, prefix=f'order_{order.id}'))
#                 for order in orders
#             ]

#             def generate_period_data(days_back, interval):
#                 base = now()
#                 result = []
#                 for i in range(days_back):
#                     if interval == 'day':
#                         start = base - timedelta(days=i + 1)
#                         end = base - timedelta(days=i)
#                         label = start.strftime('%d.%m')
#                     elif interval == 'week':
#                         start = base - timedelta(weeks=i + 1)
#                         end = base - timedelta(weeks=i)
#                         label = f"Неделя {end.strftime('%W')}"
#                     elif interval == 'month':
#                         end = (base.replace(day=1) - timedelta(days=1)).replace(day=1)
#                         start = (end - timedelta(days=30 * i)).replace(day=1)
#                         label = start.strftime('%b %Y')
#                     else:
#                         continue

#                     total = orders.filter(created_at__gte=start, created_at__lt=end).aggregate(
#                         revenue=Sum('total_price')
#                     )['revenue'] or 0

#                     result.append({'label': label, 'revenue': float(total)})

#                 return list(reversed(result))

#             import json

#             context['chart_data'] = json.dumps({
#                 'day': generate_period_data(7, 'day'),
#                 'week': generate_period_data(4, 'week'),
#                 'month': generate_period_data(6, 'month'),
#             }, default=str)

#         else:
#             context['order_forms'] = []

#         return context
