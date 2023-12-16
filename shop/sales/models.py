from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    count = models.PositiveIntegerField()
    date_delivery = models.DateField()
    unit_price = models.FloatField(default=0)









