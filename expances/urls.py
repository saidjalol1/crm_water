from django.urls import path
from .views import ExpancesView, DebtsView

app_name = "expances_app"

urlpatterns = [
    path("", ExpancesView.as_view(), name="expances_view"),
    path("debts", DebtsView.as_view(), name="debts_view")
]
