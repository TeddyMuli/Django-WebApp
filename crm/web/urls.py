from django.urls import path
from .import views


urlpatterns = [
   path('', views.home, name='home'),
   path('register/', views.register_user, name="register"),
   path('logout/', views.logout_user, name='logout'),
   path('cust_entry/', views.cust_entry, name='cust_entry'),
   path('sale_entry/', views.sale_entry, name='sale_entry'),
   path('customer_record/', views.customer_record, name='customer_record'),
   path('sale_record/', views.sale_record, name='sale_record'),
   path('customer/<customer>', views.customer, name="customer"),
   path('delete/<customer>', views.delete_record, name="delete"),
   path('update/<customer>', views.update, name="update"),
   path('pay_debt/<customer>/', views.debt, name='pay_debt'),
]
