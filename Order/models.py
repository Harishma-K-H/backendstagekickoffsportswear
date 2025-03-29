from django.db import models
from user_auth.models import Item,Customer,User

# Create your models here.
class Orderdata(models.Model):
    ORDER_STATUS = [
        ('Pending', 'Pending'),
        ('Inprogress', 'Inprogress'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    ]
    orderID = models.CharField(max_length=100, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    net_cost=models.CharField(max_length=30,null=True,blank=True)
    gst=models.CharField(max_length=30,null=True,blank=True)
    total_cost=models.CharField(max_length=30,null=True,blank=True)
    delivery_date = models.DateField()
    logo = models.FileField(upload_to='logos/', null=True, blank=True)
    front_matter = models.CharField(max_length=255, null=True, blank=True)
    front_img = models.FileField(upload_to='front_images/', null=True, blank=True)
    back_matter = models.CharField(max_length=255, null=True, blank=True)
    back_img = models.FileField(upload_to='back_images/', null=True, blank=True)
    Completed_payment=models.BooleanField(default=False)
    invoice_flag=models.BooleanField(default=False)
    status=models.CharField(max_length=100,choices=ORDER_STATUS,default="Pending",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(null=True, blank=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="created_by_order")

class OrderItem(models.Model):
    order = models.ForeignKey(Orderdata, on_delete=models.CASCADE, related_name='order_items',null=True,blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,blank=True,null=True)
    size = models.CharField(max_length=50)
    qty = models.PositiveIntegerField(null=True,blank=True)
    discount=models.CharField(max_length=50,null=True,blank=True)
    total_item_cost=models.CharField(max_length=50,null=True,blank=True)
    sleeve_case = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
class OrderPayment(models.Model):
    order_id=models.ForeignKey(Orderdata,on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    total_amount=models.CharField(max_length=100,null=True,blank=True)
    balance_amount=models.CharField(max_length=100,null=True,blank=True)
    paid_amount=models.CharField(max_length=100,null=True,blank=True)
    payment_method= models.CharField(max_length=100,null=True,blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="payment_created_by")
    def __str__(self):
        return self.order_id.orderID


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=100, unique=True) # Unique identifier for the invoice
    order = models.ForeignKey(Orderdata, on_delete=models.CASCADE,null=True,blank=True)  # Link to the Order
    order_item_id= models.ForeignKey(OrderItem, on_delete=models.CASCADE,null=True,blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Cost with decimals
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount percentage
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # GST percentage
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when invoice is created
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="created_by_invoice")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True,blank=True)
    net_cost=models.CharField(max_length=30,null=True,blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    logo = models.FileField(upload_to='logos/', null=True, blank=True)
    front_matter = models.CharField(max_length=255, null=True, blank=True)
    front_img = models.FileField(upload_to='front_images/', null=True, blank=True)
    back_matter = models.CharField(max_length=255, null=True, blank=True)
    back_img = models.FileField(upload_to='back_images/', null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.invoice_id} for Order {self.order.orderID}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,null=True,blank=True)  # Link to the Invoice
    item = models.ForeignKey(Item,on_delete=models.CASCADE,null=True,blank=True)  # Reference to the item
    size = models.CharField(max_length=50,null=True,blank=True)
    qty = models.PositiveIntegerField(null=True,blank=True)
    discount=models.CharField(max_length=50,null=True,blank=True)
    sleeve_case = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"InvoiceItem: {self.item} ({self.size}) - {self.qty} in Invoice {self.invoice.invoice_id}"