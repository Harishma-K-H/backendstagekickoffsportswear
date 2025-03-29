from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Orderdata, OrderItem,OrderPayment
from user_auth.serializers import ItemSerializer,CustomerSerializer
from user_auth.models import Item,User,Customer
class OrderItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_id', 'size', 'qty', 'sleeve_case']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()
    created_by=serializers.SerializerMethodField()

    class Meta:
        model = Orderdata
        fields = [
            'id', 'orderID', 'customer', 'order_date', 'delivery_date','net_cost','gst','total_cost', 
            'is_active', 'items','payment_details','remarks','created_by'
        ]


    def get_items(self, obj):
        order_items = obj.order_items.all()  # Fetch related OrderItem objects
        return [
            {
                'id': item.item.id,
                'name': item.item.name if item.item and item.item.name else None,
                'model': item.item.model.name if item.item and item.item.model else None,
                'code': item.item.item_code,
                'unit_cost':item.item.item_cost if item.item and item.item.item_cost else None,
                'material': item.item.material.name,  # Assuming material is a foreign key
                'print_type': item.item.print_type.name,  # Assuming print_type is a foreign key
                'sleeve_case': item.sleeve_case if item.sleeve_case else None,
                'size': item.size,
                'qty': item.qty,
                'discount': item.discount,
                'total_item_cost': item.total_item_cost
            }
            for item in order_items
        ]
    def get_customer(self, obj):
        """Fetch and return customer details."""
        if obj.customer:  # Ensure customer exists
            return {
                'id': obj.customer.id,
                'custom_id': obj.customer.custom_id,
                'name': obj.customer.name,
                'business_name': obj.customer.business_name,
                'address1': obj.customer.address1,
                'address2': obj.customer.address2,
                'mobile_number1': obj.customer.mobile_number1,
                'mobile_number2': obj.customer.mobile_number2,
                'email': obj.customer.email,
                'gst_no': obj.customer.gst_no,
            }
        return None  # If customer is missing
    def get_payment_details(self, obj):
        """Fetch all payments related to this order."""
        payments = OrderPayment.objects.filter(order_id=obj).order_by('created_at')  # ✅ Get all payments in order
        if payments.exists():
            return [
                {
                    'total_amount': payment.total_amount,
                    'balance_amount': payment.balance_amount,
                    'paid_amount': payment.paid_amount,
                    'payment_method': payment.payment_method,
                    'created_at': payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'created_by': payment.created_by.username if payment.created_by else None,
                }
                for payment in payments
            ]
        return []  # ✅ Return empty list if no payments
    def get_created_by(self, obj):
        if obj.created_by and isinstance(obj.created_by, User):  # Ensure it's a User instance
            return {
                'id': obj.created_by.id,  # ✅ Get User ID as an integer
                'name': obj.created_by.get_full_name(),  # ✅ Fetch full name
                'branch':obj.created_by.branch.name if obj.created_by.branch else None
            }
        return None 
