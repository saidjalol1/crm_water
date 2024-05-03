from django.urls import path
from .views import ExpancesView

app_name = "expances_app"

urlpatterns = [
    path("", ExpancesView.as_view(), name="expances_view")
]
