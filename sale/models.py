from django.db import models
from warehouse.models import Product

class Sale(models.Model):
    name = models.CharField(max_length=250)
    product_name = models.ForeignKey(Product, related_name="sales",on_delete=models.CASCADE)
    product_amount = models.IntegerField(default=0)
    payment_type = models.CharField(max_length=200)
    deadline = models.DateField(auto_now_add=True)
    date_added = models.DateField(auto_now_add=True)
    
    def get_overall(self):
        result = self.product_name.overall_price() * self.product_amount
        return result
    
    def get_income(self):
        result = self.product_name.overall_income() * self.product_amount
        return result
    
    def __str__(self):
        return self.name