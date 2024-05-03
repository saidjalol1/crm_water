from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi:")
    body_price = models.IntegerField(default=0, verbose_name="Tan Narxi")
    income = models.IntegerField(default=0, verbose_name="Sof Foydasi")
    amount = models.IntegerField(default=0, verbose_name="Miqdori")
    measurement_unit = models.CharField(max_length=10, verbose_name="O'lchov Birligi")
    date_added = models.DateField(auto_now_add=True)
    date_added_with_hour = models.DateTimeField(auto_now_add=True)
    
    
    def calculate_percentage(self):
        total_amount_all_products = sum([i.amount for i in Product.objects.all()])
        if total_amount_all_products:
            num = (self.amount / total_amount_all_products) * 100
            return round(num, 1)
        else:
            return 0
    
    def __str__(self):
        return self.name
