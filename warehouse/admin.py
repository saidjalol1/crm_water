from django.contrib import admin
from .models import Product, Storage

admin.site.register(Product)


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("name",)}
    
