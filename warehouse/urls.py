from django.urls import path
from .views import StorageView

app_name = "storage"

urlpatterns = [
    path("<str:slug>/", StorageView.as_view(), name="storage")
]
