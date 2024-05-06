from django.db import models


class Storage(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi:", blank=True)
    body_price = models.IntegerField(default=0, verbose_name="Tan Narxi", blank=True)
    income = models.IntegerField(default=0, verbose_name="Sof Foydasi", blank=True)
    amount = models.IntegerField(default=0, verbose_name="Miqdori", blank=True)
    measurement_unit = models.CharField(max_length=10, verbose_name="O'lchov Birligi", blank=True)
    date_added = models.DateField(auto_now_add=True, blank=True)
    date_added_with_hour = models.DateTimeField(auto_now_add=True, blank=True)
    
    max_amount = models.IntegerField(default=0, verbose_name="Limiti", blank=True)
    storage = models.ForeignKey(Storage, verbose_name="Ombori", on_delete=models.CASCADE, related_name='items')
    
    
    def calculate_percentage(self):
        total_amount_all_products = sum([i.amount for i in Product.objects.all()])
        if total_amount_all_products:
            num = (self.amount / self.max_amount ) * 100
            return round(num, 1)
        else:
            return 0
    
    def __str__(self):
        return self.name
