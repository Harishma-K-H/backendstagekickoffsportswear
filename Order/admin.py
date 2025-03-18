from django.contrib import admin
from .models import Orderdata,OrderItem,OrderPayment
# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Orderdata)
admin.site.register(OrderPayment)