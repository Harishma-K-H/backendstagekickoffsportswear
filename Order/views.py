from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Orderdata, OrderItem,OrderPayment,Invoice
from .serializers import OrderSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Max 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from user_auth.models import Item,Branch,User,Customer,MaterialData,PrintType,Material
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import now 
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db import transaction
from django.conf import settings
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated

class InvoiceList(APIView):
    def post(self, request, *args, **kwargs):
        print("📌 Request Data:", request.data)
        try:
            # Extract order details
            inovice_no=request.data.get('invoice_id')
            order_id = request.data.get('orderID')
            # customer_id = request.data.get('customer')
            delivery_date = request.data.get('delivery_date')
            net_cost=request.data.get('net_cost')
            # Fetch GST percentage from settings (default 5%)
            GST_PERCENTAGE = getattr(settings, 'GST_PERCENTAGE', 5)
            if net_cost:
                net_cost_decimal = Decimal(net_cost)  # Convert to Decimal
                gst_value = (Decimal(GST_PERCENTAGE) / 100) * net_cost_decimal
                total_cost = net_cost_decimal + gst_value
            
            # Convert delivery_date to correct format
            try:
                delivery_date = datetime.strptime(delivery_date, "%d-%m-%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY."}, status=400)

            # Validate required fields
            if not all([order_id, customer_id, delivery_date]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Get customer object
            customer = get_object_or_404(Customer, id=customer_id)

            # Ensure order is only created if at least one item matches
            with transaction.atomic():
                items_created = []
                index = 0
                valid_item_found = False  # Flag to check if at least one item is created

                while f'items[{index}][name]' in request.data:
                    try:
                        item_name = request.data.get(f'items[{index}][name]')
                        material_id = request.data.get(f'items[{index}][material]')
                        print_type_id = request.data.get(f'items[{index}][print_type]')
                        sleeve_case = request.data.get(f'items[{index}][sleeve_case]')
                        size = request.data.get(f'items[{index}][size]')
                        qty = request.data.get(f'items[{index}][qty]')

                        print(f"🔍 Processing item[{index}] - Name: {item_name}, Material: {material_id}, Print Type: {print_type_id}, Sleeve: {sleeve_case}, Size: {size}, Qty: {qty}")
                        if sleeve_case is not None:  # Ensure it's not None
                            if not all([item_name, material_id, print_type_id, sleeve_case]):
                                return Response({"error": f"Missing required fields for item[{index}]"},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            if not all([item_name, material_id, print_type_id]):  # Check without sleeve_case
                                return Response({"error": f"Missing required fields for item[{index}]"},
                                                status=status.HTTP_400_BAD_REQUEST)

                        # Ensure safe handling of sleeve_case before filtering Item
                        item_obj = Item.objects.filter(
                            name=item_name,
                            material_id=material_id,
                            print_type_id=print_type_id,
                            is_sleeve__iexact=sleeve_case.strip() if sleeve_case else None  # Avoid strip() error
                        ).first()

                        if not item_obj:
                            return Response({"error": f"No matching item found for item[{index}]"},
                                            status=status.HTTP_404_NOT_FOUND)

                        # If at least one valid item is found, create the order (if not already created)
                        if not valid_item_found:
                            order = Orderdata.objects.create(
                                orderID=order_id,
                                customer=customer,
                                delivery_date=delivery_date,
                                net_cost=str(net_cost_decimal),  # Convert Decimal to String
                                gst=str(gst_value),  # Convert Decimal to String
                                total_cost=str(total_cost),  # Convert Decimal to String
                                logo=request.FILES.get('logo'),
                                front_matter=request.data.get('front_matter'),
                                front_img=request.FILES.get('front_img'),
                                back_matter=request.data.get('back_matter'),
                                back_img=request.FILES.get('back_img')
                            )
                            valid_item_found = True  # Flag to indicate that order is now created
                            print(f"✅ Order Created: {order.orderID}")

                        # Create OrderItem entry
                        order_item = OrderItem.objects.create(
                            order=order,
                            item=item_obj,
                            size=size,
                            qty=int(qty),
                            sleeve_case=sleeve_case
                        )
                        print(f"✅ OrderItem Created: {order_item}")
                        
                        # Append item details to response
                        items_created.append({
                            "item_id": item_obj.id,
                            "name": item_obj.name,
                            "size": size,
                            "qty": qty,
                            "sleeve_case": sleeve_case,
                            "material": item_obj.material.name,
                            "print_type": item_obj.print_type.name
                        })

                        index += 1  # Move to next item

                    except Exception as e:
                        return Response({"error": f"Error processing item[{index}]: {str(e)}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                # If no valid items found, return an error response
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

# Create your views here.
class CreateOrderAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    def get(self, request, order_id=None):
        # q_data=request.query_params.get()
        if order_id:
            try:
                order = Orderdata.objects.get(orderID=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Orderdata.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Orderdata.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    parser_classes = (MultiPartParser, FormParser)  # Support file uploads

    def post(self, request, *args, **kwargs):
        print("📌 Request Data:", request.data)
        try:
            # Extract order details
            order_id = request.data.get('orderID')
            customer_id = request.data.get('customer')
            delivery_date = request.data.get('delivery_date')
            net_cost=request.data.get('net_cost')
            # Fetch GST percentage from settings (default 5%)
            GST_PERCENTAGE = getattr(settings, 'GST_PERCENTAGE', 5)
            if net_cost:
                net_cost_decimal = Decimal(net_cost)  # Convert to Decimal
                gst_value = (Decimal(GST_PERCENTAGE) / 100) * net_cost_decimal
                total_cost = net_cost_decimal + gst_value
            
            # Convert delivery_date to correct format
            try:
                delivery_date = datetime.strptime(delivery_date, "%d-%m-%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY."}, status=400)

            # Validate required fields
            if not all([order_id, customer_id, delivery_date]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Get customer object
            customer = get_object_or_404(Customer, id=customer_id)

            # Ensure order is only created if at least one item matches
            with transaction.atomic():
                items_created = []
                index = 0
                valid_item_found = False  # Flag to check if at least one item is created

                while f'items[{index}][name]' in request.data:
                    try:
                        item_name = request.data.get(f'items[{index}][name]')
                        material_id = request.data.get(f'items[{index}][material]')
                        print_type_id = request.data.get(f'items[{index}][print_type]')
                        sleeve_case = request.data.get(f'items[{index}][sleeve_case]')
                        size = request.data.get(f'items[{index}][size]')
                        qty = request.data.get(f'items[{index}][qty]')

                        print(f"🔍 Processing item[{index}] - Name: {item_name}, Material: {material_id}, Print Type: {print_type_id}, Sleeve: {sleeve_case}, Size: {size}, Qty: {qty}")
                        if sleeve_case is not None:  # Ensure it's not None
                            if not all([item_name, material_id, print_type_id, sleeve_case]):
                                return Response({"error": f"Missing required fields for item[{index}]"},
                                                status=status.HTTP_400_BAD_REQUEST)
                        else:
                            if not all([item_name, material_id, print_type_id]):  # Check without sleeve_case
                                return Response({"error": f"Missing required fields for item[{index}]"},
                                                status=status.HTTP_400_BAD_REQUEST)

                        # Ensure safe handling of sleeve_case before filtering Item
                        item_obj = Item.objects.filter(
                            name=item_name,
                            material_id=material_id,
                            print_type_id=print_type_id,
                            is_sleeve__iexact=sleeve_case.strip() if sleeve_case else None  # Avoid strip() error
                        ).first()

                        if not item_obj:
                            return Response({"error": f"No matching item found for item[{index}]"},
                                            status=status.HTTP_404_NOT_FOUND)

                        # If at least one valid item is found, create the order (if not already created)
                        if not valid_item_found:
                            order = Orderdata.objects.create(
                                orderID=order_id,
                                customer=customer,
                                delivery_date=delivery_date,
                                net_cost=str(net_cost_decimal),  # Convert Decimal to String
                                gst=str(gst_value),  # Convert Decimal to String
                                total_cost=str(total_cost),  # Convert Decimal to String
                                logo=request.FILES.get('logo'),
                                front_matter=request.data.get('front_matter'),
                                front_img=request.FILES.get('front_img'),
                                back_matter=request.data.get('back_matter'),
                                back_img=request.FILES.get('back_img')
                            )
                            valid_item_found = True  # Flag to indicate that order is now created
                            print(f"✅ Order Created: {order.orderID}")

                        # Create OrderItem entry
                        order_item = OrderItem.objects.create(
                            order=order,
                            item=item_obj,
                            size=size,
                            qty=int(qty),
                            sleeve_case=sleeve_case
                        )
                        print(f"✅ OrderItem Created: {order_item}")
                        
                        # Append item details to response
                        items_created.append({
                            "item_id": item_obj.id,
                            "name": item_obj.name,
                            "size": size,
                            "qty": qty,
                            "sleeve_case": sleeve_case,
                            "material": item_obj.material.name,
                            "print_type": item_obj.print_type.name
                        })

                        index += 1  # Move to next item

                    except Exception as e:
                        return Response({"error": f"Error processing item[{index}]: {str(e)}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                # If no valid items found, return an error response
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
    def put(self, request, *args, **kwargs):
        print("📌 Update Request Data:", request.data)

        try:
            # Extract order ID from request
            order_id = request.data.get('orderID')
            if not order_id:
                return Response({"error": "Order ID is required"}, status=400)
            
            # Fetch the Orderdata instance
            order = get_object_or_404(Orderdata, id=order_id)

            # ✅ Update Orderdata fields (if provided)
            delivery_date = request.data.get('delivery_date', None)
            customer_name = request.data.get('customer', None)
            # total_price = request.data.get('total_price', None)
            net_cost=request.data.get('net_cost', None)
            # gst=request.data.get('gst', None)
            if customer_name:
                customer = get_object_or_404(Customer, id=customer_name)

            if delivery_date:
                order.delivery_date = delivery_date
            if customer_name:
                order.customer = customer
            GST_PERCENTAGE = getattr(settings, 'GST_PERCENTAGE', 5)
            if net_cost:
                net_cost_decimal = Decimal(net_cost)  # Convert to Decimal
                gst_value = (Decimal(GST_PERCENTAGE) / 100) * net_cost_decimal
                total_cost = net_cost_decimal + gst_value
                order.total_cost=total_cost

            # if total_price:
            #     try:
            #         order.total_cost = float(total_price)
            #     except ValueError:
            #         return Response({"error": "Invalid total price format"}, status=400)

            order.save()  # Save the updated order details

            # ✅ Update OrderItem records
            index = 0  # Track item index for debugging
            updated_items = []  # Store updated item details

            while f'items[{index}][item_id]' in request.data:
                try:
                    item_id = request.data.get(f'items[{index}][item_id]')
                    if not item_id:
                        return Response({"error": f"Missing item_id at index {index}"}, status=400)

                    # Fetch the existing OrderItem
                    order_item = get_object_or_404(OrderItem, order=order, item_id=item_id)

                    # Get the fields from the request (if provided)
                    material_id = request.data.get(f'items[{index}][material]', None)
                    print_type_id = request.data.get(f'items[{index}][print_type]', None)
                    size = request.data.get(f'items[{index}][size]', None)
                    qty = request.data.get(f'items[{index}][qty]', None)
                    sleeve_case = request.data.get(f'items[{index}][sleeve_case]', None)

                    # ✅ Update OrderItem fields only if new values are provided
                    if material_id:
                        material = get_object_or_404(MaterialData, id=material_id)
                        order_item.item.material = material
                    if print_type_id:
                        print_type = get_object_or_404(PrintType, id=print_type_id)
                        order_item.item.print_type = print_type
                    if size:
                        order_item.size = size
                    if qty:
                        try:
                            order_item.qty = int(qty)
                        except ValueError:
                            return Response({"error": f"Invalid quantity format for item[{index}]"}, status=400)
                    if sleeve_case:
                        order_item.sleeve_case = sleeve_case
                    if not order_item.created_at:
                        order_item.created_at = now()  # Set current timestamp

                    # Save updates
                    order_item.item.save()
                    order_item.save()

                    # Store updated item details
                    updated_items.append({
                        "item_id": order_item.item.id,
                        "name": order_item.item.name,
                        "size": order_item.size,
                        "qty": order_item.qty,
                        "sleeve_case": order_item.sleeve_case,
                        "material": order_item.item.material.name if order_item.item.material else None,
                        "print_type": order_item.item.print_type.name if order_item.item.print_type else None
                    })

                    index += 1  # Move to the next item
                
                except Exception as e:
                    return Response({"error": f"Error processing item[{index}]: {str(e)}"}, status=400)

            return Response({
                "message": "Order and order items updated successfully!",
                # "orderID": order.id,
                # "updated_order": {
                #     "customer_name": order.customer.name,
                #     "total_price": order.total_cost
                # },
                # "updated_items": updated_items
            }, status=200)

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
@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for this view
class OrderPaymentAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access

    def post(self, request):
        if request.user and isinstance(request.user, AnonymousUser):
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        order_id = request.data.get('order_id')

        #  Handle missing order_id properly
        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Orderdata.objects.get(id=order_id)
        except Orderdata.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        #  Convert to float for proper comparison
        try:
            total_amount = float(request.data.get('total_amount', 0))
            balance_amount = float(request.data.get('balance_amount', 0))
            paid_amount = float(request.data.get('paid_amount', 0))
        except ValueError:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method')

        #  Create payment entry
        payments = OrderPayment.objects.create(
            order_id=order,
            total_amount=total_amount,
            balance_amount=balance_amount,
            paid_amount=paid_amount,
            payment_method=payment_method,
            created_by=request.user
        )
        payments.save()

        # Update order payment status
        if balance_amount == 0 or total_amount == paid_amount:
            order.Completed_payment = True
            order.save()  # Ensure order is updated in the database

        return Response({'message': 'Payment Successful'}, status=status.HTTP_201_CREATED)
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