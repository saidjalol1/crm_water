from django.urls import path
from .views import SaleView

app_name = "sale"

urlpatterns = [
    path("", SaleView.as_view(), name="sale_view"),
]
