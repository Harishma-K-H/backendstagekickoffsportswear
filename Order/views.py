from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Orderdata, OrderItem,OrderPayment,Invoice,InvoiceItem
from .serializers import OrderSerializer,InvoiceSerializer,OrderSerializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Max 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from user_auth.models import Item,Branch,User,Customer,MaterialData,PrintType,Material,models,Model_data,State,ShippingCustomer
import random
from django.db.models import Q
import json
from django.utils import timezone
from datetime import date, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now 
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)
import traceback
from datetime import datetime
from django.db import transaction
from django.conf import settings
from django.db.models.functions import Cast
from django.db.models import Sum
from decimal import Decimal
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
import uuid
from user_auth.pagination import CustomPagination
from decimal import Decimal,InvalidOperation, ROUND_HALF_UP, getcontext
from .utils import generate_upi_qr_code
from django.db import IntegrityError  
from django.db.models import Sum, DecimalField
from django.db.models.functions import ExtractMonth, ExtractYear
def generate_invoice_id(user):
    try:
        branch_code = user.branch.code.upper()
    except AttributeError:
        raise ValueError("User does not have a valid branch associated.")

    default_invoice_ids = {
        "CLT": "CLT-0081",
        "KKL": "KKL-0147",
        "MJR": "MJR-0037",
        "TCR": "TCR-0009",
        "EKM": "EKM-0096",
    }

    with transaction.atomic():
        # Fetch all invoice IDs for this branch
        branch_invoices = Orderdata.objects.filter(invoice_id__startswith=branch_code)
        
        max_number = 0
        for order in branch_invoices:
            try:
                num = int(order.invoice_id.split("-")[-1])
                max_number = max(max_number, num)
            except (ValueError, AttributeError):
                continue

        if max_number == 0:
            max_number = int(default_invoice_ids[branch_code].split("-")[-1])

        next_number = max_number + 1
        return f"{branch_code}-{str(next_number).zfill(4)}"
# class GetInvoiceNumberAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure user is authenticated

#     def generate_order_number(self, branch):
       
#         # Get the last order for this branch
#         last_order = Orderdata.objects.filter(orderID__startswith=f"{branch.code}").aggregate(Max('orderID'))
        
#         if last_order['orderID__max']:
#             # Extract last number and increment it
#             last_number = int(last_order['orderID__max'].split('/')[-1])
#             new_number = last_number + 1
#         else:
#             new_number = 1  # Start from 0001 if no previous orders

#         return f"{branch.code}{new_number:04d}"

#     def get(self, request, *args, **kwargs):
#         """Fetch the next order number for the request user's branch"""

#         # Get the user's branch
#         user_branch = request.user.branch

#         if not user_branch:
#             return Response({"error": "User is not associated with any branch."}, status=400)

#         # Generate order number for user's branch
#         order_number = self.generate_order_number(user_branch)

#         return Response({"order_number": order_number}, status=200)
class InvoiceView(APIView):
    def get(self, request, invoice_id=None, *args, **kwargs):
        try:
            # ✅ Fetch the invoice by ID
            try:
                # Try to fetch the invoice by its id
                invoice = Invoice.objects.get(id=invoice_id)
            except Invoice.DoesNotExist:
                return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)
            items = InvoiceItem.objects.filter(invoice=invoice)
            total_paid = OrderPayment.objects.filter(order_id=invoice.order) \
                .annotate(paid_amount_decimal=Cast('paid_amount', models.DecimalField(max_digits=10, decimal_places=2))) \
                .aggregate(Sum('paid_amount_decimal'))['paid_amount_decimal__sum'] or 0
	    #  Prepare invoice response
            items_qs = (
                InvoiceItem.objects
                .filter(invoice=invoice)
                .select_related(
                    "item",
                    "item__model",
                    "item__material",
                    "item__print_type",
                )
            )

            # ✅ Compute total cost ONCE for all items
            items_total_cost = (
                items_qs
                .aggregate(
                    total=Sum(Cast("total_item_cost", DecimalField(max_digits=12, decimal_places=2)))
                )["total"] or Decimal("0")
            )
            # ✅ Prepare invoice response
            invoice_data = {
                'id':invoice.id,
                "invoice_id": invoice.invoice_id,
                "order_id": invoice.order.id,
                "orderID": invoice.order.orderID,
                "invoice_satus":invoice.order.order_invoice if invoice.order else None,
                "discount":invoice.order.discount,
                'remarks':invoice.order.remarks,
                "items_total_cost": str(items_total_cost), 
                "customer": {
                    'custom_id': invoice.order.customer.id if invoice.order.customer else None,
                    'business_name': invoice.order.customer.business_name if invoice.order.customer else None,
                    'address1': invoice.order.customer.address1 if invoice.order.customer else None,
                    'address2': invoice.order.customer.address2 if invoice.order.customer else None,
                    'mobile_number1': invoice.order.customer.mobile_number1 if invoice.order.customer else None,
                    'mobile_number2': invoice.order.customer.mobile_number2 if invoice.order.customer else None,
                    'email': invoice.order.customer.email if invoice.order.customer else None,
                    'gst_no': invoice.order.customer.gst_no if invoice.order.customer and invoice.order.customer.state else None,
                    'state_name': invoice.order.customer.state.name if invoice.order.customer and invoice.order.customer.state else None,
                    'pincode': invoice.order.customer.pincode if invoice.order.customer else None
                },
                "delivery_date": invoice.delivery_date.strftime("%d-%m-%Y"),
                "net_cost": str(invoice.net_cost),
                "gst": str(invoice.gst),
                "created_at": invoice.created_at,
                "created_by": {
                    "id": invoice.created_by.id if invoice.created_by else None,
                    "name": invoice.created_by.get_full_name() if invoice.created_by else "Unknown",
                    "branch": invoice.created_by.branch.name if invoice.created_by and invoice.created_by.branch else "N/A",
                    "logo": invoice.created_by.branch.logo.url if invoice.created_by and invoice.created_by.branch.logo else None,
                    "pincode": invoice.created_by.branch.pincode if invoice.created_by and invoice.created_by.branch else "N/A",
                    "state": invoice.created_by.branch.state if invoice.created_by and invoice.created_by.branch else "N/A",
                    "GSTN": invoice.created_by.branch.GSTN if invoice.created_by and invoice.created_by.branch else "N/A",
                    "email": invoice.created_by.branch.email if invoice.created_by and invoice.created_by.branch else "N/A",
                    "phn_no": invoice.created_by.branch.phn_no if invoice.created_by and invoice.created_by.branch else "N/A",
                    'account_details':invoice.created_by.branch.account_details if invoice.created_by and invoice.created_by.branch else "N/A",
                    # 'qr_code': invoice.created_by.branch.qr_code.url if invoice.created_by and invoice.created_by.branch and invoice.created_by.branch.qr_code else "N/A",

                    "city": invoice.created_by.branch.city if invoice.created_by and invoice.created_by.branch else "N/A",
                    "address":invoice.created_by.branch.location if invoice.created_by and invoice.created_by.branch else "N/A",
                    "district": invoice.created_by.branch.district if invoice.created_by and invoice.created_by.branch else "N/A",
                    } if invoice.created_by else None,
                "total_cost": str(invoice.total_cost),
                "total_paid_amount": str(total_paid),
                "items": []
            }

            # ✅ Loop through invoice items
            for item in items:
                # Default unit cost as None (in case it's not found)
                unit_cost = None

                # ✅ Check if the item exists with matching conditions
                query = Item.objects.filter(
                    name=item.item.name,
                    material=item.item.material,
                    print_type=item.item.print_type
                )
                print("TESTSTTTTT",query)

                # ✅ Check if sleeve_case should be included
                if item.item.name not in ["SHORTS", "LOWER"]:
                    query = query.filter(is_sleeve=item.sleeve_case)

                matched_item = query.first()
                
                if matched_item:
                    unit_cost = str(matched_item.item_cost)  # Convert to string for JSON response

                # ✅ Append item details to the response
                invoice_data["items"].append({
                    "item_id": item.item.id,
                    "name": item.item.name,
                    "model":item.item.model.name,
                    'item_cost':round(float(item.total_item_cost) / item.qty, 2),
                    "size": item.size,
                    "HSN":item.item.HSN,
                    'discount':item.discount,
                    "total_item_cost":item.total_item_cost,
                    "qty": item.qty,
                    "sleeve_case": item.item.is_sleeve if item.item else None,
                    "material": item.item.material.name if item.item and item.item.material else None,
                    "print_type": item.item.print_type.name,
                    # "unit_cost": unit_cost   # ✅ Add unit cost to response
                })

            return Response(invoice_data, status=status.HTTP_200_OK)

        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.dateformat import format
from .models import Invoice, InvoiceItem
from user_auth.pagination import CustomPagination
from django.db.models import Prefetch

class InvoiceList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        # Base queryset
        invoices = Invoice.objects.select_related(
            'order', 'customer', 'created_by', 'created_by__branch'
        ).prefetch_related(
            Prefetch('invoice_items', queryset=InvoiceItem.objects.select_related('item__model', 'item__material', 'item__print_type', 'item'))
        ).exclude(order__status='Canceled')

        if user.role.name != "Admin":
            invoices = invoices.filter(created_by__branch__id=user.branch.id)

        # Month/year filtering
        if month and year:
            try:
                month = int(month)
                year = int(year)
                if 1 <= month <= 12:
                    invoices = invoices.annotate(
                        invoice_month=ExtractMonth('created_at'),
                        invoice_year=ExtractYear('created_at')
                    ).filter(invoice_month=month, invoice_year=year)
                else:
                    return Response({"error": "Invalid month (1-12)"}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Month and year must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        invoices = invoices.order_by('-invoice_id')

        # Pagination
        paginator = CustomPagination()
        paginated_invoices = paginator.paginate_queryset(invoices, request)

        # Build response
        invoice_data = []
        for invoice in paginated_invoices:
            customer = invoice.customer
            order = invoice.order
            created_by = invoice.created_by
            branch = created_by.branch if created_by else None
            items = invoice.invoice_items.all()

            invoice_data.append({
                "id": invoice.id,
                "invoice_id": invoice.invoice_id,
                "invoice_generated": invoice.invoice_generated,
                "order_id": invoice.order_id,
                "orderID": order.orderID if order else None,
                "invoice_satus":order.order_invoice if order else None,
                "order_amount": str(order.total_cost) if order else None,
                "customer": {
                    "custom_id": customer.id if customer else None,
                    "email": customer.email if customer else None,
                    "phn": customer.mobile_number1 if customer else None,
                    "name": customer.name if customer else None,
                    "business_name": customer.business_name if customer else None,
                    "mobile_number1": customer.mobile_number1 if customer else None,
                    "mobile_number2": customer.mobile_number2 if customer else None,
                    "address1": customer.address1 if customer else None,
                    "address2": customer.address2 if customer else None,
                    "gst_no": customer.gst_no if customer else None,
                    "pincode":customer.pincode if customer else None
                },
                "delivery_date": invoice.delivery_date.strftime("%d-%m-%Y") if invoice.delivery_date else None,
                "net_cost": str(invoice.net_cost),
                "gst": str(invoice.gst),
                "total_cost": str(invoice.total_cost),
                "created_at": invoice.created_at,
                "created_by": {
                    "id": created_by.id if created_by else None,
                    "name": created_by.get_full_name() if created_by else "Unknown",
                    "branch": branch.name if branch else "No Branch",
                    "branch_city": branch.city if branch else "No City",
                },
                "items": [
                    {
                        "item_id": item.item.id,
                        "name": item.item.name,
                        "modal": item.item.model.name if item.item.model else None,
                        "unit_cost": str(item.item.item_cost),
                        "total_item_cost": str(item.total_item_cost),
                        "discount": item.discount,
                        "size": item.size,
                        "qty": item.qty,
                        "sleeve_case": item.sleeve_case,
                        "material": item.item.material.name if item.item.material else None,
                        "print_type": item.item.print_type.name if item.item.print_type else None,
                    }
                    for item in items
                ],
            })

        if not invoice_data:
            return Response({"message": "No invoices found."}, status=status.HTTP_204_NO_CONTENT)

        return paginator.get_paginated_response(invoice_data)
    def post(self, request, *args, **kwargs):
        print("DEBUG: Received request data ->", request.data)
        try:
            order_id = request.data.get('orderID')
            customer_id = request.data.get('customer')
            delivery_date = request.data.get('delivery_date')
            net_cost = request.data.get('net_cost')

            net_cost_decimal = Decimal(net_cost) if net_cost else Decimal(0)

            GST_PERCENTAGE = getattr(settings, 'GST_PERCENTAGE', 5)
            gst_value = (Decimal(GST_PERCENTAGE) / 100) * net_cost_decimal
            total_cost = net_cost_decimal + gst_value
            # Round total cost to nearest whole number (e.g., 136.50 → 137)
            total_cost = total_cost.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            try:
                order=Orderdata.objects.get(id=order_id)
            except Orderdata.DoesNotExist:
                return Response({'error':"Order does not exisit"})

            try:
                delivery_date = datetime.strptime(delivery_date, "%d-%m-%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use DD-MM-YYYY."}, status=400)

            if not all([order_id, customer_id, delivery_date]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Check if an invoice already exists for this order
            existing_invoice = Invoice.objects.filter(order_id=order_id).first()
            if existing_invoice:
                return Response({"error": "Invoice already generated for this order."}, status=400)

            customer = get_object_or_404(Customer, id=customer_id)

            with transaction.atomic():
                items_created = []
                errors = []
                valid_item_found = False

                # ✅ Generate custom invoice ID
                # invoice_id = generate_invoice_id(request.user)  # Use custom function

                invoice = Invoice.objects.create(
                    invoice_id=order.invoice_id,  # ✅ Custom Invoice ID
                    order_id=order_id,
                    customer=customer,
                    delivery_date=delivery_date,
                    net_cost=net_cost_decimal,
                    gst=gst_value,
                    total_cost=total_cost,
                    logo=request.FILES.get('logo', None),
                    front_matter=request.data.get('front_matter', ''),
                    front_img=request.FILES.get('front_img', None),
                    back_matter=request.data.get('back_matter', ''),
                    back_img=request.FILES.get('back_img', None),
                    created_by=request.user
                )

                index = 0
                while f'items[{index}][name]' in request.data:
                    try:
                        item_name = request.data.get(f'items[{index}][name]')
                        model_id=request.data.get(f'items[{index}][model]')
                        material_id = request.data.get(f'items[{index}][material]')
                        print_type_id = request.data.get(f'items[{index}][print_type]')
                        sleeve_case = request.data.get(f'items[{index}][sleeve_case]', False)
                        size = request.data.get(f'items[{index}][size]')
                        qty = request.data.get(f'items[{index}][qty]', 0)

                        qty = int(qty) if qty else 0

                        item_obj = Item.objects.filter(
                            name=item_name,
                            model=model_id,
                            material_id=material_id,
                            print_type_id=print_type_id,
                            is_sleeve=sleeve_case
                        ).first()

                        if not item_obj:
                            errors.append(f"No matching item found for item[{index}]")
                            index += 1
                            continue  

                        InvoiceItem.objects.create(
                            invoice=invoice,
                            item=item_obj,
                            size=size,
                            qty=qty,
                            sleeve_case=sleeve_case
                        )

                        items_created.append({
                            "item_id": item_obj.id,
                            "name": item_obj.name,
                            "size": size,
                            "qty": qty,
                            "sleeve_case": sleeve_case,
                            "material": item_obj.material.name,
                            "print_type": item_obj.print_type.name
                        })

                        valid_item_found = True

                    except Exception as e:
                        errors.append(f"Error processing item[{index}]: {str(e)}")

                    index += 1

                if not valid_item_found:
                    invoice.delete()  
                    return Response({"error": "No matching items found, invoice not created."}, status=400)

                if errors:
                    return Response({"errors": errors}, status=400)

            return Response({
                "message": f"Invoice {invoice_id} created successfully!",
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
class CreateOrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self, user):
        """Role-based queryset with optimizations"""
        if user.role.name == "Admin":
            return Orderdata.objects.select_related(
                'created_by__branch'
            ).exclude(status='Canceled').order_by('-id')

        return Orderdata.objects.select_related(
            'created_by__branch'
        ).filter(
            created_by__branch__id=user.branch.id
        ).exclude(status='Canceled').order_by('-id')

    def get(self, request, order_id=None):
        user = request.user

        if order_id:
            order = Orderdata.objects.filter(orderID=order_id).select_related(
                'created_by__branch'
            ).first()
            if not order:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Get paginated order list
        orders = self.get_queryset(user)
        paginator = CustomPagination()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializers(paginated_orders, many=True)

        # log_user_activity(request, "Fetched orders list")
        return paginator.get_paginated_response(serializer.data)
    def post(self, request, *args, **kwargs):
        print("📌 Request Data:", request.data)
        try:
            branch = request.user.branch
            order_id = request.data.get('orderID')
            customer_id = request.data.get('customer')
            shipped_id=request.data.get('shipped')
            delivery_date = request.data.get('delivery_date')
            net_cost = request.data.get('net_cost')
            remarks = request.data.get('remarks')
            order_discount=request.data.get('discount')
            is_exist = str(request.data.get('is_exist')).lower() == 'true'
            sh_is_exist = str(request.data.get('sh_is_exist')).lower() == 'true'

          
            GST_PERCENTAGE = getattr(settings, 'GST_PERCENTAGE', 5)
            if net_cost:
                net_cost_decimal = Decimal(net_cost)
                gst_value = (Decimal(GST_PERCENTAGE) / 100) * net_cost_decimal
                total_cost = net_cost_decimal + gst_value
                # Round total cost to nearest whole number (e.g., 136.50 → 137)
                total_cost = total_cost.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

            try:
                delivery_date = datetime.strptime(delivery_date, "%d-%m-%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY."}, status=400)

            if not all([order_id, delivery_date]):
                return Response({"errors": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            if not is_exist:
                state_id = request.data.get('state')
                try:
                    state_instance = State.objects.get(id=state_id) if state_id else None
                except State.DoesNotExist:
                    state_instance = None
                try:
                    customer = Customer.objects.create(
                        address1=request.data.get('address1'),
                        address2=request.data.get('address2'),
                        address3=request.data.get('address3'),
                        pincode=request.data.get('pincode'),
                        business_name=request.data.get('business_name'),
                        email=request.data.get('email'),
                        gst_no=request.data.get('gst_no'),
                        mobile_number1=request.data.get('mobile_number1'),
                        mobile_number2=request.data.get('mobile_number2'),
                        name=request.data.get('name'),
                        state=state_instance
                    )
                
                    customer.save()
                except IntegrityError as e:
                    if 'unique constraint' in str(e).lower() or 'duplicate' in str(e).lower():
                        return Response({"error": "Mobile number already exists"}, status=400)
            else:
                customer = get_object_or_404(Customer, id=customer_id)
            if not sh_is_exist:
                state_id = request.data.get('sh_state')
                try:
                    state_instance = State.objects.get(id=state_id) if state_id else None
                except State.DoesNotExist:
                    state_instance = None
                # shipment=ShippingCustomer.objects.create(
                #     address1=request.data.get('sh_address1'),
                #     address2=request.data.get('sh_address2'),
                #     business_name=request.data.get('sh_business_name'),
                #     email=request.data.get('sh_email'),
                #     gst_no=request.data.get('sh_gst_no'),
                #     mobile_number1=request.data.get('sh_mobile_number1'),
                #     mobile_number2=request.data.get('sh_mobile_number2'),
                #     name=request.data.get('sh_name'),
                #     # custom_id=customer,
                #     state=state_instance


                # )
                # shipment.save()
            # else:
            #     shipment=ShippingCustomer.objects.create(
            #         address1=customer.address1,
            #         address2=customer.address2,
            #         business_name=customer.business_name,
            #         email=customer.email,
            #         gst_no=customer.gst_no,
            #         mobile_number1=customer.mobile_number1,
            #         mobile_number2=customer.mobile_number2,
            #         name=customer.name,
            #         custom_id=customer,
            #         # state=state_instance


            #     )
            #     shipment.save()

            with transaction.atomic():
                items_created = []
                index = 0
                valid_item_found = False

                while f'items[{index}][name]' in request.data:
                    try:
                        item_name = request.data.get(f'items[{index}][name]')
                        model_id = request.data.get(f'items[{index}][model]')
                        material_id = request.data.get(f'items[{index}][material]')
                        print_type_id = request.data.get(f'items[{index}][print_type]')
                        sleeve_case = request.data.get(f'items[{index}][sleeve_case]')
                        discount = request.data.get(f'items[{index}][discount]')
                        total_item_cost = request.data.get(f'items[{index}][total_item_cost]')
                        size = request.data.get(f'items[{index}][size]')
                        qty = request.data.get(f'items[{index}][qty]')

                        print(f"🔍 Processing item[{index}] - Name: {item_name}, Model: {model_id}, Material: {material_id}, Print Type: {print_type_id}, Sleeve: {sleeve_case}, Size: {size}, Qty: {qty}")

                        if not all([item_name, model_id]):
                            return Response({"error": f"Missing required fields for item[{index}]"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        #  Dynamic filter logic
                        filter_kwargs = {
                            "name": item_name,
                            "model_id": model_id,
                            "branch": branch
                        }

                        # Only add material_id if provided and valid
                        if material_id and material_id.lower() != 'undefined':
                            try:
                                filter_kwargs["material_id"] = int(material_id)  # Convert to integer
                            except ValueError:
                                return Response({"error": f"Invalid material ID for item[{index}]"}, 
                                                status=status.HTTP_400_BAD_REQUEST)

                        # Only add print_type_id if provided and valid
                        if print_type_id and print_type_id.lower() != 'undefined':
                            try:
                                filter_kwargs["print_type_id"] = int(print_type_id)  # Convert to integer
                            except ValueError:
                                return Response({"error": f"Invalid print type ID for item[{index}]"}, 
                                                status=status.HTTP_400_BAD_REQUEST)

                        # Only add sleeve_case if provided and valid
                        if sleeve_case and sleeve_case.lower() != 'undefined':
                            filter_kwargs["is_sleeve__iexact"] = sleeve_case.strip()

                        print("🔍 Final Filter Criteria:", filter_kwargs)

                        item_obj = Item.objects.filter(**filter_kwargs).first()

                        if not item_obj:
                            return Response({"error": f"No matching item found for item[{index}]"},
                                            status=status.HTTP_404_NOT_FOUND)
                        # upi_id = branch.upi_id  # Your new field
                        # amount = total_cost  # Whatever logic gives total invoice amount

                        # Generate QR code and attach
                        # qr_code_image = generate_upi_qr_code(upi_id, amount)
                        if not valid_item_found:
                            order = Orderdata.objects.create(
                                orderID=order_id,
                                customer=customer,
                                # shipped_customer=shipment,
                                delivery_date=delivery_date,
                                remarks=remarks,
                                net_cost=str(net_cost_decimal),
                                gst=str(gst_value),
                                total_cost=str(total_cost),
                                discount=order_discount,
                                # invoice_id=generate_invoice_id(request.user),
                                # qr_code = qr_code_image,
                                logo=request.FILES.get('logo'),
                                front_matter=request.data.get('front_matter'),
                                front_img=request.FILES.get('front_img'),
                                back_matter=request.data.get('back_matter'),
                                back_img=request.FILES.get('back_img'),
                                status="Pending",
                                created_by=request.user
                            )
                            valid_item_found = True
                            print(f" Order Created: {order.orderID}")

                        order_item = OrderItem.objects.create(
                            order=order,
                            item=item_obj,
                            size=size,
                            discount=discount,
                            total_item_cost=total_item_cost,
                            qty=int(qty),
                            sleeve_case=sleeve_case
                        )
                        print(f" OrderItem Created: {order_item}")

                        items_created.append({
                            "item_id": item_obj.id,
                            "name": item_obj.name,
                            "size": size,
                            "qty": qty,
                            "sleeve_case": sleeve_case,
                            "model": item_obj.model.name,
                            "material": item_obj.material.name if item_obj.material else None,
                            "print_type": item_obj.print_type.name if item_obj.print_type else None
                        })

                        index += 1

                    except Exception as e:
                        return Response({"error": f"Error processing item[{index}]: {str(e)}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                if not valid_item_found:
                    return Response({"error": "No matching items found, order not created."},
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "orderID": order.orderID,
                "message": "Order created successfully!",
                "items": items_created
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class DetailedOrderAPIView (APIView): 
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    def get(slef,request,order_id):
        try:
            order = Orderdata.objects.get(id=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Orderdata.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            
    # parser_classes = (MultiPartParser, FormParser)  # Supports file uploads
class OrderItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def clean_id(self, value):
        if value in [None, '', 'null', 'undefined']:
            return None
        return value

    def put(self, request, *args, **kwargs):
        print("📌 Update Request Data:", request.data)

        q_data = request.query_params.get('data')

        # ================== INVOICE GENERATION ==================
        if q_data == "generated":
            order_id = self.clean_id(request.data.get('orderID'))

            if not order_id:
                return Response({"error": "Order ID is required"}, status=400)

            orders = Orderdata.objects.all()
            role_name = getattr(getattr(request.user, "role", None), "name", None)
            if role_name != "Admin":
                if request.user.branch_id is None:
                    raise PermissionDenied("Your user account is not assigned to a branch.")
                orders = orders.filter(created_by__branch=request.user.branch)
            order = get_object_or_404(orders, id=order_id)

            order_invoice = request.data.get("order_invoice")
            order.order_invoice_sent_date = timezone.now()
            order.order_invoice = order_invoice

            if order.invoice_id:
                invoice_id = order.invoice_id
            else:
                invoice_id = generate_invoice_id(request.user)
                order.invoice_id = invoice_id

            order.save()

            invoice = Invoice.objects.filter(invoice_id=invoice_id).first()

            if not invoice:
                invoice = Invoice.objects.create(
                    invoice_id=invoice_id,
                    order=order,
                    customer=order.customer,
                    delivery_date=order.delivery_date,
                    net_cost=order.net_cost,
                    gst=order.gst,
                    total_cost=order.total_cost,
                    created_by=request.user
                )

                for order_item in OrderItem.objects.filter(order=order):
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        item=order_item.item,
                        order_item=order_item,
                        total_item_cost=order_item.total_item_cost,
                        size=order_item.size,
                        qty=order_item.qty,
                        sleeve_case=order_item.sleeve_case
                    )

            return Response({'message': "Order Invoice processed successfully"}, status=200)

        # ================== ORDER UPDATE ==================
        try:
            order_id = self.clean_id(request.data.get('orderID'))

            if not order_id:
                return Response({"error": "Order ID is required"}, status=400)

            order = get_object_or_404(Orderdata, id=order_id)

            delivery_date = request.data.get('delivery_date')
            customer_id = self.clean_id(request.data.get('customer'))
            net_cost = request.data.get('net_cost')
            order_discount = request.data.get('discount')
            remarks = request.data.get('remarks')

            if customer_id:
                customer = get_object_or_404(Customer, id=customer_id)
                order.customer = customer

            if delivery_date:
                order.delivery_date = delivery_date

            if order_discount is not None:
                try:
                    order.discount = Decimal(order_discount)
                except:
                    return Response({"error": "Invalid discount"}, status=400)

            if remarks:
                order.remarks = remarks

            # ===== COST CALCULATION =====
            refund_message = None
            GST_PERCENTAGE = getattr(settings, 'GST_PERCENTAGE', 5)

            if net_cost is not None:
                net_cost_decimal = Decimal(str(net_cost))

                gst_value = (
                    Decimal(str(GST_PERCENTAGE)) / Decimal('100')
                ) * net_cost_decimal

                gst_value = gst_value.quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )

                total_cost = (
                    net_cost_decimal + gst_value
                ).quantize(
                    Decimal('0.01'),
                    rounding=ROUND_HALF_UP
                )

                paid_qs = OrderPayment.objects.filter(order_id=order)
                total_paid = sum(
                    Decimal(p.paid_amount or '0')
                    for p in paid_qs
                )

                if total_paid > total_cost:
                    excess_amount = total_paid - total_cost

                    OrderPayment.objects.create(
                        order_id=order,
                        customer=order.customer,
                        total_amount=str(total_cost),
                        balance_amount=str(-excess_amount),
                        paid_amount=total_paid,
                        payment_method="REFUND",
                        refund_amount=str(excess_amount),
                        created_by=request.user
                    )

                    refund_message = f"Overpaid ₹{excess_amount}"

                # ✅ IMPORTANT
                order.net_cost = net_cost_decimal
                order.gst = gst_value
                order.total_cost = total_cost

            order.save()

            # ===== UPDATE INVOICE =====
            invoice = Invoice.objects.filter(order=order).first()

            if invoice:
                invoice.total_cost = order.total_cost
                invoice.discount = order.discount
                invoice.gst = order.gst
                invoice.net_cost = order.net_cost
                invoice.delivery_date = order.delivery_date
                invoice.customer = order.customer
                invoice.save()

            # ===== DELETE ITEMS =====
            deleted_item_ids = request.data.get('deleted_item_ids', [])

            if isinstance(deleted_item_ids, str):
                try:
                    deleted_item_ids = json.loads(deleted_item_ids)
                except:
                    deleted_item_ids = []

            for order_item_id in deleted_item_ids:
                order_item_id = self.clean_id(order_item_id)

                if not order_item_id:
                    continue

                order_item = OrderItem.objects.filter(id=order_item_id, order=order).first()

                if order_item:
                    InvoiceItem.objects.filter(order_item=order_item).delete()
                    order_item.delete()

            # ===== PROCESS ITEMS =====
            index = 0

            while f'items[{index}][name]' in request.data:

                order_item_id = self.clean_id(request.data.get(f'items[{index}][item_id]'))
                item_name = request.data.get(f'items[{index}][name]')

                model_id = self.clean_id(request.data.get(f'items[{index}][model]'))
                material_id = self.clean_id(request.data.get(f'items[{index}][material]'))
                print_type_id = self.clean_id(request.data.get(f'items[{index}][print_type]'))

                size = request.data.get(f'items[{index}][size]')
                qty = request.data.get(f'items[{index}][qty]')
                sleeve_case = request.data.get(f'items[{index}][sleeve_case]')
                total_item_cost = request.data.get(f'items[{index}][total_item_cost]')
                discount = request.data.get(f'items[{index}][discount]')

                # ✅ SAFE FETCH (NO CRASH)
                model = Model_data.objects.filter(id=model_id).first() if model_id else None
                material = Material.objects.filter(id=material_id).first() if material_id else None
                print_type = PrintType.objects.filter(id=print_type_id).first() if print_type_id else None

                order_item = OrderItem.objects.filter(id=order_item_id, order=order).first() if order_item_id else None

                # ===== UPDATE EXISTING =====
                if order_item:

                    order_item.size = size
                    order_item.qty = qty
                    order_item.discount = discount
                    order_item.sleeve_case = sleeve_case
                    order_item.total_item_cost = total_item_cost
                    order_item.save()

                    # Update InvoiceItem values only
                    invoice_item = InvoiceItem.objects.filter(
                        order_item=order_item
                    ).first()

                    if invoice_item:
                        invoice_item.size = size
                        invoice_item.qty = qty
                        invoice_item.discount = discount
                        invoice_item.sleeve_case = sleeve_case
                        invoice_item.total_item_cost = total_item_cost
                        invoice_item.save()

                # ===== CREATE NEW =====
                else:
                    filters = {
                        "model": model,
                        "is_sleeve": sleeve_case,
                        "branch": request.user.branch
                    }

                    if material:
                        filters["material"] = material

                    if print_type:
                        filters["print_type"] = print_type

                    new_item = Item.objects.filter(**filters).first()

                    if not new_item:
                        return Response({"error": f"No matching Item for index {index}"}, status=400)

                    new_order_item = OrderItem.objects.create(
                        order=order,
                        item=new_item,
                        size=size,
                        qty=qty,
                        discount=discount,
                        sleeve_case=sleeve_case,
                        total_item_cost=total_item_cost,
                        created_at=now()
                    )

                    if invoice:
                        InvoiceItem.objects.create(
                            invoice=invoice,
                            item=new_item,
                            order_item=new_order_item,
                            size=size,
                            qty=qty,
                            discount=discount,
                            sleeve_case=sleeve_case,
                            total_item_cost=total_item_cost
                        )

                index += 1

            return Response({
                "message": "Order updated successfully",
                "refund_alert": refund_message
            })

        except Exception as e:
            return Response({"error": str(e)}, status=400)
    # def delete(self, request, order_id):
    #     try:
    #         # Fetch the order along with its related order items
    #         order = Orderdata.objects.get(orderID=order_id)

    #         with transaction.atomic():
    #             # Delete all order items related to this order
    #             deleted_items_count, _ = OrderItem.objects.filter(order=order).delete()

    #             # Delete the order itself
    #             order.delete()

    #         return Response({
    #             "message": "Order deleted successfully",
    #             "deleted_items": deleted_items_count
    #         }, status=status.HTTP_204_NO_CONTENT)

    #     except Orderdata.DoesNotExist:
    #         return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetNextOrderNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def generate_order_number(self, branch):
        """Generate order number in format: BRANCH_CODE/2526/0001"""

        middle_number = "2526"  # Fixed middle number, change dynamically if needed

        # Get the last order for this branch
        last_order = Orderdata.objects.filter(orderID__startswith=f"{branch.code}/{middle_number}/").aggregate(Max('orderID'))
        
        if last_order['orderID__max']:
            # Extract last number and increment it
            last_number = int(last_order['orderID__max'].split('/')[-1])
            new_number = last_number + 1
        else:
            new_number = 1  # Start from 0001 if no previous orders

        return f"{branch.code}/{middle_number}/{new_number:04d}"

    def get(self, request, *args, **kwargs):
        """Fetch the next order number for the request user's branch"""

        # Get the user's branch
        user_branch = request.user.branch

        if not user_branch:
            return Response({"error": "User is not associated with any branch."}, status=400)

        # Generate order number for user's branch
        order_number = self.generate_order_number(user_branch)

        return Response({"order_number": order_number}, status=200)
class OrderPaymentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            if not order_id:
                return Response({"error": "Order ID is required"}, status=400)

            order = Orderdata.objects.get(id=order_id)

            # ✅ Generate or use existing invoice_id
            # if order.invoice_id:
            #     invoice_id = order.invoice_id
            # else:
            #     invoice_id = generate_invoice_id(request.user)
            #     order.invoice_id = invoice_id
            #     order.save() 

            try:
                total_amount = float(request.data.get('total_amount', 0))
                balance_amount = float(request.data.get('balance_amount', 0))
                paid_amount = float(request.data.get('paid_amount', 0))
            except ValueError:
                return Response({"error": "Invalid amount format"}, status=400)

            # ✅ Create payment record
            OrderPayment.objects.create(
                order_id=order,
                customer=order.customer,
                total_amount=str(total_amount),
                balance_amount=str(balance_amount),
                paid_amount=str(paid_amount),
                refund_amount=str(request.data.get('refund_amount', '0')),
                payment_method=request.data.get('payment_method'),
                created_by=request.user
            )

            # ✅ If full payment, generate invoice (only if not exists)
            if abs(balance_amount) < 0.01 or abs(total_amount - paid_amount) < 0.01:
                order.Completed_payment = True
                order.order_invoice = "PAID"
                # ✅ Generate or use existing invoice_id
                if order.invoice_id:
                    invoice_id = order.invoice_id
                else:
                    invoice_id = generate_invoice_id(request.user)
                    order.invoice_id = invoice_id
                    order.save() 
                order.order_invoice_sent_date = timezone.now()
                order.save()
                existing_invoice = Invoice.objects.filter(invoice_id=invoice_id).first()
                if existing_invoice:
                    print("kjkjkjkjkjkjkjk")
                    existing_invoice.invoice_generated=True
                    existing_invoice.save()
                
                else:
                    invoice = Invoice.objects.create(
                        invoice_id=invoice_id,
                        order=order,
                        customer=order.customer,
                        delivery_date=order.delivery_date,
                        net_cost=order.net_cost,
                        gst=order.gst,
                        invoice_generated=True,
                        total_cost=order.total_cost,
                        created_by=request.user
                    )

                    # ✅ Create invoice items
                    for order_item in OrderItem.objects.filter(order=order):
                        InvoiceItem.objects.create(
                            invoice=invoice,
                            item=order_item.item,
                            total_item_cost=order_item.total_item_cost,
                            size=order_item.size,
                            qty=order_item.qty,
                            sleeve_case=order_item.sleeve_case
                        )
            return Response({"message": "Payment recorded successfully."}, status=201)

        except Exception as e:
            logger.error(f"Payment API error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                "error": str(e),
                "trace": traceback.format_exc()
            }, status=500)
class OrderPaymentDetails(APIView):
    def get(self, request, order_id):
        # Fetch payment details for the given order_id
        payment_details = OrderPayment.objects.filter(order_id=order_id)

        # Convert queryset to list of dictionaries
        payment_data = []
        for data in payment_details:
            payment_data.append({
                'id': data.id,
                'order_id': data.order_id.id,  # Access the order ID properly
                'total_amount': data.total_amount,
                'balance_amount': data.balance_amount,
                'paid_amount': data.paid_amount,
                'payment_method': data.payment_method,
            })

        return Response(payment_data, status=200)
    
class CustomerDetails(APIView):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response({'error': "Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Get all orders for the customer
        customer_orders = Orderdata.objects.filter(customer=customer)
        orders_serializer = OrderSerializer(customer_orders, many=True)

        # Get all invoices related to the customer's orders
        customer_invoices = Invoice.objects.filter(order__in=customer_orders)
        invoices_serializer = InvoiceSerializer(customer_invoices, many=True)

        return Response({
            'customer_id': pk,
            'business_name':customer.business_name,
            'orders': orders_serializer.data,
            'invoices': invoices_serializer.data
        }, status=status.HTTP_200_OK)

class OrderByDeliveryDateAPIView(APIView):
    def get(self, request):
        user=request.user
        date_param = request.query_params.get('date')

        if date_param == 'today':
            target_date = date.today()
        elif date_param == 'tomorrow':
            target_date = date.today() + timedelta(days=1)
        else:
            return Response({'error': 'Invalid date param. Use "today" or "tomorrow".'}, status=status.HTTP_400_BAD_REQUEST)
        if user.role.name == "Admin":
            orders = Orderdata.objects.filter(delivery_date=target_date, is_active=True)
            print("admin based")
            serializer = OrderSerializer(orders, many=True)
        else:
            orders = Orderdata.objects.filter(created_by__branch__id=user.branch.id,delivery_date=target_date, is_active=True).order_by('-id')
            print("branch based")
            serializer = OrderSerializer(orders, many=True)
        # log_user_activity(request, "Logged in successfully")
        return Response({
            "date": str(target_date),
            "orders": serializer.data
        }, status=status.HTTP_200_OK)
class InvoiceReportAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("DATA",request.data)
        branch = request.user.branch
        q_data = request.query_params.get('data')
        branch_id_param = request.query_params.get('branch_id')
        print("branchpassign",branch_id_param)

        invoices = Invoice.objects.filter(
        ).select_related(
            'order', 'customer', 'created_by'
        ).prefetch_related(
            'invoice_items'
        ).order_by('-invoice_id')

        if q_data == "paid_invoices":
            invoices = invoices.filter(order__Completed_payment=True)
        elif q_data == "unpaid_invoices":
            if request.user.role.name.lower() == "admin":
                if branch_id_param:
                    invoices = invoices.filter(order__Completed_payment=False, order__created_by__branch__id=branch_id_param)
            else:
                invoices = invoices.filter(order__Completed_payment=False, order__created_by__branch=branch)

        # Pagination
        paginator = CustomPagination()
        paginated_invoices = paginator.paginate_queryset(invoices, request)

        # Serialize
        serializer = InvoiceSerializer(paginated_invoices, many=True)

        # Add payment info from OrderPayment
        enriched_data = []
        for invoice in serializer.data:
            order_id = invoice.get('order_id')
            payment = OrderPayment.objects.filter(order_id__orderID=order_id).first()

            invoice['paid_amount'] = float(payment.paid_amount) if payment and payment.paid_amount else 0.00
            invoice['balance_amount'] = float(invoice['total_cost']) - float(invoice['paid_amount'])

            enriched_data.append(invoice)

        return paginator.get_paginated_response(enriched_data)
class CanceledOrdersAPI(APIView):

    def put(self, request, order_id):
        try:
            order = get_object_or_404(Orderdata, id=order_id)

            # Already canceled check
            if order.status == "Canceled":
                return Response({
                    "message": "Order already canceled"
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update status
            order.status = "Canceled"

            # Optional: save remarks from request
            remarks = request.data.get("remarks")
            if remarks:
                order.remarks = remarks

            order.save()

            return Response({
                "message": "Order canceled successfully",
                "order_id": order.id,
                "status": order.status
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
