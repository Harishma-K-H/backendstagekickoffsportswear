from django.contrib import admin
from .models import Orderdata,OrderItem,OrderPayment,Invoice,InvoiceItem
# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Orderdata)
admin.site.register(OrderPayment)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)