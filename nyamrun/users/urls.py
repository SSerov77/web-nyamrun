from django.urls import path
from django.contrib.auth import views

import users.views
from users.forms import CustomAuthenticationForm, CustomPasswordChangeForm


urlpatterns = [
    path('signup/', users.views.signup, name='signup'),
    path(
        'login/',
        views.LoginView.as_view(
            template_name='users/login.html',
            authentication_form=CustomAuthenticationForm
        ),
        name='login'
    ),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', users.views.ProfileView.as_view(), name='profile'),
    path('manager/profile/', users.views.ManagerProfileView.as_view(), name='manager_profile'),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            form_class=CustomPasswordChangeForm
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'),

]
