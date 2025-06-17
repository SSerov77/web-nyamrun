import users.views
from django.contrib.auth import views
from django.urls import path
from users.forms import CustomAuthenticationForm, CustomPasswordChangeForm

urlpatterns = [
    path("signup/", users.views.signup, name="signup"),
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", users.views.ProfileView.as_view(), name="profile"),
    path(
        "manager/profile/",
        users.views.ManagerProfileView.as_view(),
        name="manager_profile",
    ),
    path(
        "manager/orders/<int:order_id>/status/",
        users.views.ManagerOrderStatusUpdateView.as_view(),
        name="manager-order-update-status",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            form_class=CustomPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("privacy_policy/", users.views.privacy_policy, name="privacy_policy"),
    path(
        "cookie_usage_policy/",
        users.views.cookie_usage_policy,
        name="cookie_usage_policy"
    ),
    path(
        "terms_of_use/", users.views.terms_of_use, name="terms_of_use"
    ),
]
