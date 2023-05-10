from django.contrib import admin
from .models import Record, Sale, Route,Product

admin.site.register(Record)
admin.site.register(Sale)
admin.site.register(Route)
admin.site.register(Product)