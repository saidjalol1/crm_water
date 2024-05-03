from django.db import models

class Expances(models.Model):
    name = models.CharField(max_length=250, verbose_name="Mijozning Ismi")
    amount = models.FloatField(default=0, verbose_name="summasi")
    currency = models.CharField(max_length=100,default="so'm")
    deadline = models.DateField(auto_now_add=True)
    date_added = models.DateField(auto_now_add=True, verbose_name="Sanansi")
    payment_type = models.CharField(max_length=250, verbose_name="To'lov turi")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    extra_phone_number = models.CharField(max_length=20, verbose_name="Qo'shimcha raqam")
    
    
    def __str__(self):
        return self.name
    
    
    
