from django.db import models
from django.db.models import Sum


class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=50, unique=True, db_index=True, primary_key=True)
    def __str__(self):
        return self.phone_no

class Sale(models.Model):
    f_name = models.CharField(max_length=50)
    client = models.ForeignKey(Record, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    def __str__(self):
        return self.price
