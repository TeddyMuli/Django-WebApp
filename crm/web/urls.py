from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


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
   path('debt_record/', views.debt_record, name="debt_record"),
   path('financials/', views.financials, name="financials"),
   path('expense/', views.expense, name="expense"),
   path('expense_record/', views.expense_record, name="expense_record"),
   path('search', views.search_customer, name="search_customer"),
   path('login/', views.login_n, name="login"),
   path('send_bulk_sms/', views.send_bulk_sms, name="send_bulk_sms"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)