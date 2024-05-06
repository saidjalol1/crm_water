from .models import Storage

def storages(request):
    return {"storages":Storage.objects.all()}