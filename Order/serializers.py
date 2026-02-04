from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Orderdata, OrderItem,OrderPayment,Invoice,InvoiceItem
from user_auth.serializers import ItemSerializer,CustomerSerializer
from user_auth.models import Item,User,Customer
from decimal import Decimal
class OrderItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_id', 'size', 'qty', 'sleeve_case']

class OrderSerializers(serializers.ModelSerializer):
    # items = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    # payment_details = serializers.SerializerMethodField()
    # created_by=serializers.SerializerMethodField()
    # shipped_customer=serializers.SerializerMethodField()
    items_total_cost = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
 

    class Meta:
        model = Orderdata
        fields = [
            'id', 'orderID', 'customer', 'order_date', 'delivery_date','net_cost','gst','total_cost', 
            'is_active','remarks','invoice_id','discount','items_total_cost','created_at','order_invoice',
            'order_invoice_sent_date','Completed_payment'
        ]
    def get_created_at(self, obj):
        invoice = Invoice.objects.filter(order=obj).order_by('-created_at').first()
        if invoice and invoice.created_at:
            return invoice.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        return None
    def get_items_total_cost(self, obj):
        total = 0.0
        for item in obj.order_items.all():
            try:
                total += float(item.total_item_cost or 0)
            except (ValueError, TypeError):
                continue
        return round(total, 2)
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
                'address3':obj.customer.address3,
                'mobile_number1': obj.customer.mobile_number1,
                'mobile_number2': obj.customer.mobile_number2,
                'email': obj.customer.email,
                'gst_no': obj.customer.gst_no,
                'state_name': obj.customer.state.name if obj.customer.state else None,  # Fixed here
                'pincode':obj.customer.pincode if obj.customer.pincode else None
            }
        return None  # If customer is missing
    
    def get_shipped_customer(self, obj):
        if obj.shipped_customer:
            return {
                'id': obj.shipped_customer.id,
                'custom_id': obj.shipped_customer.custom_id.id if obj.shipped_customer.custom_id else None,
                'name': obj.shipped_customer.name,
                'business_name': obj.shipped_customer.business_name,
                'address1': obj.shipped_customer.address1,
                'address2': obj.shipped_customer.address2,
                'mobile_number1': obj.shipped_customer.mobile_number1,
                'mobile_number2': obj.shipped_customer.mobile_number2,
                'email': obj.shipped_customer.email,
                'gst_no': obj.shipped_customer.gst_no,
                'state_name': obj.shipped_customer.state.name if obj.shipped_customer.state else None,
            }
        return None
    # def get_payment_details(self, obj):
    #     """Fetch all payments related to this order."""
    #     payments = OrderPayment.objects.filter(order_id=obj).order_by('created_at')  # ✅ Get all payments in order
    #     if payments.exists():
    #         return [
    #             {
    #                 'total_amount': payment.total_amount,
    #                 'balance_amount': payment.balance_amount,
    #                 'paid_amount': payment.paid_amount,
    #                 'payment_method': payment.payment_method,
    #                 'created_at': payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    #                 'created_by': payment.created_by.username if payment.created_by else None,
    #                 'refund':payment.refund_amount if payment.refund_amount else None
    #             }
    #             for payment in payments
    #         ]
    #     return []  # ✅ Return empty list if no payments
    def get_created_by(self, obj):
        if obj.created_by and isinstance(obj.created_by, User):  # Ensure it's a User instance
            return {
                'id': obj.created_by.id,  # ✅ Get User ID as an integer
                'name': obj.created_by.get_full_name(),  # ✅ Fetch full name
                'branch':obj.created_by.branch.name if obj.created_by.branch else None,
                'pincode':obj.created_by.branch.pincode if obj.created_by.branch else None,
                'state': obj.created_by.branch.state if obj.created_by.branch else None,
                'GSTN':obj.created_by.branch.GSTN if obj.created_by.branch else None,
                'email':obj.created_by.branch.email if obj.created_by.branch else None,
                'phn_no':obj.created_by.branch.phn_no if obj.created_by.branch else None,
                'logo': obj.created_by.branch.logo.url if obj.created_by.branch and obj.created_by.branch.logo else None,
                'account_details':obj.created_by.branch.account_details if obj.created_by and obj.created_by.branch else "N/A",
                'code':obj.created_by.branch.code if obj.created_by.branch else None,
                'city':obj.created_by.branch.city if obj.created_by.branch else None,
                'address':obj.created_by.branch.location if obj.created_by.branch else None,
                'district':obj.created_by.branch.district if obj.created_by.branch else None
            }
        return None 
class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()
    created_by=serializers.SerializerMethodField()
    shipped_customer=serializers.SerializerMethodField()
    items_total_cost = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Orderdata
        fields = [
            'id', 'orderID', 'customer', 'order_date', 'delivery_date','net_cost','gst','total_cost', 
            'is_active', 'items','payment_details','remarks','Completed_payment','created_by','invoice_id','discount','shipped_customer','items_total_cost','created_at','order_invoice','order_invoice_sent_date'
        ]
    def get_created_at(self, obj):
        invoice = Invoice.objects.filter(order=obj).order_by('-created_at').first()
        if invoice and invoice.created_at:
            return invoice.created_at.strftime('%Y-%m-%dT%H:%M:%S')
        return None

    def get_items_total_cost(self, obj):
        total = 0.0
        for item in obj.order_items.all():
            try:
                total += float(item.total_item_cost or 0)
            except (ValueError, TypeError):
                continue
        return round(total, 2)
    def get_items(self, obj):
        order_items = obj.order_items.all()  # Fetch related OrderItem objects
        return [
            {
                'id': item.item.id,
                'order_item_id':item.id,
                'name': item.item.name if item.item and item.item.name else None,
                'model': item.item.model.name if item.item and item.item.model else None,
                'code': item.item.item_code,
                'unit_cost': item.item.item_cost if item.item and item.item.item_cost else None,
                'material': item.item.material.name if item.item and item.item.material else None,  # Accessing material from the related Item
                'material_id': item.item.material.id if item.item and item.item.material else None,
                'print_type': item.item.print_type.name if item.item and item.item.print_type else None,  # Accessing print_type from the related Item
                'print_type_id': item.item.print_type.id if item.item and item.item.print_type else None,
                'sleeve_case': item.sleeve_case if item.sleeve_case else None,
                'size': item.size,
                'HSN':item.item.HSN,
                'qty': item.qty,
                'discount': item.discount,
                'total_item_cost': item.total_item_cost,
                'item_cost': round(float(item.total_item_cost) / item.qty, 2)
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
                'address3':obj.customer.address3,
                'mobile_number1': obj.customer.mobile_number1,
                'mobile_number2': obj.customer.mobile_number2,
                'email': obj.customer.email,
                'gst_no': obj.customer.gst_no,
                'state_name': obj.customer.state.name if obj.customer.state else None,  # Fixed here
                'pincode':obj.customer.pincode if obj.customer.pincode else None
            }
        return None  # If customer is missing
    
    def get_shipped_customer(self, obj):
        if obj.shipped_customer:
            return {
                'id': obj.shipped_customer.id,
                'custom_id': obj.shipped_customer.custom_id.id if obj.shipped_customer.custom_id else None,
                'name': obj.shipped_customer.name,
                'business_name': obj.shipped_customer.business_name,
                'address1': obj.shipped_customer.address1,
                'address2': obj.shipped_customer.address2,
                'mobile_number1': obj.shipped_customer.mobile_number1,
                'mobile_number2': obj.shipped_customer.mobile_number2,
                'email': obj.shipped_customer.email,
                'gst_no': obj.shipped_customer.gst_no,
                'state_name': obj.shipped_customer.state.name if obj.shipped_customer.state else None,
            }
        return None
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
                    'refund':payment.refund_amount if payment.refund_amount else None
                }
                for payment in payments
            ]
        return []  # ✅ Return empty list if no payments
    def get_created_by(self, obj):
        if obj.created_by and isinstance(obj.created_by, User):  # Ensure it's a User instance
            return {
                'id': obj.created_by.id,  # ✅ Get User ID as an integer
                'name': obj.created_by.get_full_name(),  # ✅ Fetch full name
                'branch':obj.created_by.branch.name if obj.created_by.branch else None,
                'pincode':obj.created_by.branch.pincode if obj.created_by.branch else None,
                'state': obj.created_by.branch.state if obj.created_by.branch else None,
                'GSTN':obj.created_by.branch.GSTN if obj.created_by.branch else None,
                'email':obj.created_by.branch.email if obj.created_by.branch else None,
                'phn_no':obj.created_by.branch.phn_no if obj.created_by.branch else None,
                'logo': obj.created_by.branch.logo.url if obj.created_by.branch and obj.created_by.branch.logo else None,
                'account_details':obj.created_by.branch.account_details if obj.created_by and obj.created_by.branch else "N/A",
                'code':obj.created_by.branch.code if obj.created_by.branch else None,
                'city':obj.created_by.branch.city if obj.created_by.branch else None,
                'address':obj.created_by.branch.location if obj.created_by.branch else None,
                'district':obj.created_by.branch.district if obj.created_by.branch else None
            }
        return None 

class InvoiceItemSerializer(serializers.ModelSerializer):
    model=serializers.CharField(source="item.model.name",read_only=True)
    material=serializers.CharField(source="item.material.name",read_only=True)
    print_type=serializers.CharField(source="item.print_type.name",read_only=True)
    unit_cost = serializers.SerializerMethodField()
    def get_unit_cost(self, obj):
        try:
            return round(float(obj.total_item_cost) / obj.qty, 2) if obj.qty else 0.0
        except (ZeroDivisionError, TypeError, AttributeError):
            return 0.0
    class Meta:
        model = InvoiceItem
        fields = '__all__'
class InvoiceSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True, read_only=True)
    order_id = serializers.CharField(source='order.orderID', read_only=True)
    customer_name = serializers.CharField(source='customer.business_name', read_only=True)
    total_paid_amount = serializers.SerializerMethodField()
    balance_amount = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_id', 'order', 'order_item_id', 'total_cost', 'discount', 'gst',
            'created_at', 'created_by', 'customer', 'net_cost', 'delivery_date',
            'logo', 'front_matter', 'front_img', 'back_matter', 'back_img',
            'order_id', 'invoice_items','invoice_generated','customer_name','total_paid_amount', 'balance_amount'
        ]
    def get_total_paid_amount(self, obj):
        payment = OrderPayment.objects.filter(order_id=obj.order).first()
        return payment.paid_amount if payment else "0"

    def get_balance_amount(self, obj):
        payment = OrderPayment.objects.filter(order_id=obj.order).first()
        total_cost = obj.total_cost
        print("jdhkddjdjddddddddddddddddddddddddddddddddddddd",total_cost)
        paid = Decimal(payment.paid_amount) if payment and payment.paid_amount else Decimal("0.00")
        print("kkkkkkkkkkkkkkkkkkkkkkk",paid)
        
        balance_amount = total_cost - paid
        return balance_amount
