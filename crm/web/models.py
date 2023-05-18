from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

    
class Route(models.Model):
    route = models.CharField(max_length=50)
    def __str__(self):
        return self.route
    
class Product(models.Model):
    product = models.CharField(max_length=50)
    price = models.IntegerField()
    def __str__(self):
        return f"{self.product} @Ksh:{self.price}"
    
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=10, unique=True, db_index=True, primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    def __str__(self):
        return f"{self.f_name} {self.l_name}"

PAY = (
    ('M-PESA' , 'M-PESA'),
    ('CASH' , 'CASH'),
)

class Sale(models.Model):
    client = models.ForeignKey(Record, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    served_by = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    paid = models.IntegerField()
    pay = models.CharField(max_length=10,choices=PAY)

    @property
    def price(self):
        price = self.product.price * self.quantity
        return int(price)
    
    @property
    def debt(self):
        debt = int(self.price - self.paid)
        return debt

    def __str__(self):
        return f"{self.client}"

class Debt(models.Model):
    client = models.ForeignKey(Record, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.client}"