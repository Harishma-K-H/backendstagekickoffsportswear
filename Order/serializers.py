from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Orderdata, OrderItem
from user_auth.serializers import ItemSerializer,CustomerSerializer
from user_auth.models import Item,User,Customer
class OrderItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_id', 'size', 'qty', 'sleeve_case']

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Orderdata
        fields = [
            'id', 'orderID', 'customer', 'order_date', 'delivery_date', 'logo', 
            'front_matter', 'front_img', 'back_matter', 'back_img', 'is_active', 'items'
        ]

    def get_items(self, obj):
        order_items = obj.order_items.all()  # Fetch related OrderItem objects
        return [
            {
                'id': item.item.id,
                'name': item.item.name,
                'code': item.item.item_code,
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

  