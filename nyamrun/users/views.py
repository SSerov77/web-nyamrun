from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from orders.models import Order
from users.forms import CustomUserCreationForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем последние 10 заказов пользователя
        orders = Order.objects.filter(user=self.request.user).order_by(
            '-created_at')[:10].prefetch_related(
                'items', 'items__options', 'items__product'
            )

        context.update({
            'user': self.request.user,
            'orders': orders,
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
