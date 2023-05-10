from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

    
class Route(models.Model):
    route = models.CharField(max_length=50)
    def __str__(self):
        return self.route
    

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10, unique=True, db_index=True, primary_key=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    def __str__(self):
        return self.phone_no

PAY = (
    ('M-PESA' , 'M-PESA'),
    ('CASH' , 'CASH'),
)

class Sale(models.Model):
    f_name = models.CharField(max_length=50)
    client = models.ForeignKey(Record, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    paid = models.IntegerField()
    pay = models.CharField(max_length=10,choices=PAY)
    served_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def debt(self):
        debt = int(self.price - self.paid)
        return debt
    
    def __str__(self):
        return self.price

class Product(models.Model):
    product = models.CharField(max_length=50)
    price = models.IntegerField()
    def __str__(self):
        return self.product