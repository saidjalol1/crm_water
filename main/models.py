from django.db import models



class Expance(models.Model):
    name = models.CharField(max_length=250)
    amount = models.IntegerField(default=0)
    currency = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    
    