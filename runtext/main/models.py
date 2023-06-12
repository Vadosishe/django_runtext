from django.db import models


# Create your models here.
class Car(models.Model):
    billing_number = models.BigIntegerField(primary_key=True)
    customer = models.CharField(max_length=100)
    price = models.IntegerField()
    purchase_date = models.DateTimeField()
    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.BigIntegerField()
    mfg_date = models.DateTimeField()
    shipping_date = models.DateTimeField()
