from django.contrib import admin
from .models import Record, Sale, Route,Product, Message

admin.site.register(Record)
admin.site.register(Sale)
admin.site.register(Route)
admin.site.register(Product)
admin.site.register(Message)