from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Orderdata, OrderItem
from .serializers import OrderSerializer
from django.db.models import Max 
from user_auth.models import Item,Branch,User,Customer
import random
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
# Create your views here.
class CreateOrderAPIView(APIView):
    def get(self, request, order_id=None):
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
    # parser_classes = (MultiPartParser, FormParser)  # Support file uploads

   


    def post(self, request, *args, **kwargs):
        print("📌 Request Data:", request.data)
        try:
            # Extract order details
            order_id = request.data.get('orderID')
            customer_id = request.data.get('customer')
            delivery_date = request.data.get('delivery_date')
            net_cost = request.data.get('net_cost')
            gst = request.data.get('gst')
            total_cost = request.data.get('total_cost')

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

            # Ensure order is only created if at least one valid item is found
            with transaction.atomic():
                items_created = []
                index = 0
                valid_item_found = False  # Flag to check if at least one item is created

                while f'items[{index}][name]' in request.data:
                    try:
                        item_name = request.data.get(f'items[{index}][name]')
                        material_id = request.data.get(f'items[{index}][material]')
                        print_type_id = request.data.get(f'items[{index}][print_type]')
                        sleeve_case = request.data.get(f'items[{index}][sleeve_case]')  # Optional
                        size = request.data.get(f'items[{index}][size]')
                        qty = request.data.get(f'items[{index}][qty]')
                        discount = request.data.get(f'items[{index}][discount]')
                        total_item_cost = request.data.get(f'items[{index}][total_item_cost]')

                        print(f"🔍 Processing item[{index}] - Name: {item_name}, Material: {material_id}, Print Type: {print_type_id}, Sleeve: {sleeve_case}, Size: {size}, Qty: {qty}")

                        # Validate required fields
                        if not all([item_name, material_id, print_type_id]):
                            return Response({"error": f"Missing required fields for item[{index}]"},
                                            status=status.HTTP_400_BAD_REQUEST)

                        # First, try to find an exact match including sleeve_case
                        item_obj = Item.objects.filter(
                            name=item_name,
                            material_id=material_id,
                            print_type_id=print_type_id,
                            is_sleeve__iexact=sleeve_case.strip() if sleeve_case else None
                        ).first()

                        # If no exact match, try to match without sleeve_case
                        if not item_obj:
                            item_obj = Item.objects.filter(
                                name=item_name,
                                material_id=material_id,
                                print_type_id=print_type_id
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
                                net_cost=net_cost,
                                gst=gst,
                                total_cost=total_cost,
                                logo=request.FILES.get('logo'),
                                front_matter=request.data.get('front_matter'),
                                front_img=request.FILES.get('front_img'),
                                back_matter=request.data.get('back_matter'),
                                back_img=request.FILES.get('back_img'),
                            )
                            valid_item_found = True  # Mark that order is created
                            print(f"✅ Order Created: {order.orderID}")

                        # Create OrderItem entry
                        order_item = OrderItem.objects.create(
                            order=order,
                            item=item_obj,
                            discount=discount,
                            total_item_cost=total_item_cost,
                            size=size,
                            qty=int(qty),
                            sleeve_case=sleeve_case if sleeve_case else "N/A"
                        )
                        print(f"✅ OrderItem Created: {order_item}")

                        # Append item details to response
                        items_created.append({
                            "item_id": item_obj.id,
                            "name": item_obj.name,
                            "size": size,
                            "qty": qty,
                            "sleeve_case": sleeve_case if sleeve_case else "N/A",
                            "material": item_obj.material.name,
                            "print_type": item_obj.print_type.name
                        })

                        index += 1  # Move to next item

                    except Exception as e:
                        return Response({"error": f"Error processing item[{index}]: {str(e)}"},
                                        status=status.HTTP_400_BAD_REQUEST)

                # If no valid items found, return an error response and do NOT create order
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
    def get(self, request, order_id=None):
        if order_id:
            try:
                order = Orderdata.objects.get(id=order_id)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Orderdata.DoesNotExist:
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Orderdata.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
    # parser_classes = (MultiPartParser, FormParser)  # Supports file uploads

    def put(self, request, order_id):
        print("📌 Update Request Data:", request.data)
        try:
            # order_id = request.data.get('orderID')
            item_id = request.data.get('item_id')

            # Ensure order and item exist
            order = get_object_or_404(Orderdata, id=order_id)
            order_item = get_object_or_404(OrderItem, order=order, item_id=item_id)

            # Extract new values (if provided)
            item_name = request.data.get('name', order_item.item.name)
            material_id = request.data.get('material', order_item.item.material_id)
            print_type_id = request.data.get('print_type', order_item.item.print_type_id)
            sleeve_case = request.data.get('sleeve_case', order_item.sleeve_case)
            size = request.data.get('size', order_item.size)
            qty = request.data.get('qty', order_item.qty)
            discount = request.data.get('discount', order_item.discount)  # ✅ Added discount update
            total_item_cost = request.data.get('total_item_cost', order_item.total_item_cost)  # ✅ Added cost update

            with transaction.atomic():
                # Find matching Item in the Item model
                new_item = Item.objects.filter(
                    name=item_name,
                    material_id=material_id,
                    print_type_id=print_type_id,
                    is_sleeve__iexact=sleeve_case.strip() if sleeve_case else None
                ).first()

                if not new_item:
                    return Response({"error": "No matching item found, update failed."},
                                    status=status.HTTP_404_NOT_FOUND)

                # Update OrderItem fields
                order_item.item = new_item
                order_item.size = size
                order_item.qty = int(qty) if qty else order_item.qty
                order_item.sleeve_case = sleeve_case
                order_item.discount = discount  # ✅ Added discount update
                order_item.total_item_cost = total_item_cost  # ✅ Added total cost update
                order_item.save()

            return Response({
                "message": "Order item updated successfully!",
                "orderID": order.orderID,
                "updated_item": {
                    "item_id": new_item.id,
                    "name": new_item.name,
                    "size": size,
                    "qty": qty,
                    "sleeve_case": sleeve_case,
                    "material": new_item.material.name,
                    "print_type": new_item.print_type.name,
                    "discount": discount,  # ✅ Added discount in response
                    "total_item_cost": total_item_cost  # ✅ Added total cost in response
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        try:
            # Fetch the order along with its related order items
            order = Orderdata.objects.get(orderID=order_id)

            with transaction.atomic():
                # Delete all order items related to this order
                deleted_items_count, _ = OrderItem.objects.filter(order=order).delete()

                # Delete the order itself
                order.delete()

            return Response({
                "message": "Order deleted successfully",
                "deleted_items": deleted_items_count
            }, status=status.HTTP_204_NO_CONTENT)

        except Orderdata.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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