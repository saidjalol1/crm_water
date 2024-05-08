from django.urls import path

from django.contrib.auth.views import LogoutView
from .views import LoginView, MainView, ExpanceView, DebtsView

app_name = "main_app"

urlpatterns = [
    path("", MainView.as_view(), name="main"),
    path("chiqim/", ExpanceView.as_view(), name="expance"),
    path("qarzlar/", DebtsView.as_view(), name="debts"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
