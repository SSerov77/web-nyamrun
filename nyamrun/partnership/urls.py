from django.urls import path
from partnership import views

urlpatterns = [
    path("", views.partnership, name="partnership"),
    path("submit/", views.partnership_submit, name="partnership_submit"),
]
