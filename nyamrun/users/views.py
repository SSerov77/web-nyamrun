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


class ManagerProfileView(TemplateView):
    template_name = 'users/manager_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = getattr(self.request.user, 'managed_address', None)
        context['address'] = address
        if address:
            orders = Order.objects.filter(address=address).order_by('-created_at')
            order_forms = [
                (order, OrderStatusForm(instance=order, prefix=f'order_{order.id}'))
                for order in orders
            ]
            context['order_forms'] = order_forms
        else:
            context['order_forms'] = []
        return context

    def post(self, request, *args, **kwargs):
        address = getattr(self.request.user, 'managed_address', None)
        if not address:
            return redirect('manager_profile')
        orders = Order.objects.filter(address=address)
        for order in orders:
            prefix = f'order_{order.id}'
            if f'{prefix}-status' in request.POST:
                form = OrderStatusForm(request.POST, instance=order, prefix=prefix)
                if form.is_valid():
                    form.save()
                break
        return redirect('manager_profile')