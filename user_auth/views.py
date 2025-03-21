from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Branch,User,Customer,Material,PrintType,Model_data,Item,UserRole,MaterialData,District
from .serializers import BranchSerializer,CustomTokenObtainPairSerializer,UserRoleSerializer,MaterialDataSerializer,UserSerializer,CustomerSerializer,PrintTypeSerializer,MaterialSerializer,ModelDataSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny 
from rest_framework import permissions,generics
from .permissions import IsHRUser,IsAdminOrHR
from rest_framework.exceptions import PermissionDenied
from .permissions import UserPermissions
from django.shortcuts import get_object_or_404
from django.utils import timezone 
from rest_framework import status
from decimal import Decimal
from rest_framework import viewsets
from .permissions import has_permission
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class CustomPagination(PageNumberPagination):
    page_size = 20  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class DistrictList(APIView):
    def get(self,request):
        districts = District.objects.all().values('id', 'name')

        # Remove unwanted spaces or carriage returns from names
        cleaned_districts = [{'id': d['id'], 'name': d['name'].strip()} for d in districts]

        return JsonResponse(cleaned_districts, safe=False)
class login_view(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer
    Permission_classes=[AllowAny]# Corrected permission usage
class UserView(APIView):

    # 🔹 GET: Retrieve all users
    def get(self, request):
        users = User.objects.filter(is_active=True,role__id=2)  # Get only active users
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 POST: Create a new user
    def post(self, request):
        # Check if branch is included in request data
        branch_id = request.data.get('branch')

        # Validate if the branch exists
        if branch_id:
            try:
                branch = Branch.objects.get(id=branch_id)
            except Branch.DoesNotExist:
                return Response({"branch": "Invalid branch ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Assign branch if provided
            if branch_id:
                user.branch = branch
                user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):

    # 🔹 GET: Retrieve a single user by ID
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id, is_active=True)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 PUT: Update user by ID
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)  # Get the user or return 404

        data = request.data

        # Update fields manually
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "middle_name" in data:
            user.middle_name = data["middle_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "dob" in data:
            user.dob = data["dob"]
        if "address" in data:
            user.address = data["address"]
        if "age" in data:
            user.age = data["age"]
        if "email" in data:
            user.email = data["email"]
        if "mobile_number" in data:
            user.mobile_number = data["mobile_number"]

        # Handle ForeignKey fields (Branch & Role)
        if "branch" in data:
            try:
                user.branch = Branch.objects.get(id=data["branch"])
            except Branch.DoesNotExist:
                return Response({"error": "Invalid branch ID"}, status=status.HTTP_400_BAD_REQUEST)

        if "role" in data:
            try:
                user.role = UserRole.objects.get(id=data["role"])
            except UserRole.DoesNotExist:
                return Response({"error": "Invalid role ID"}, status=status.HTTP_400_BAD_REQUEST)

        if "pro_pic" in request.FILES:
            user.pro_pic = request.FILES["pro_pic"]

        if "is_active" in data:
            user.is_active = data["is_active"]

        user.save()  # Save updated user
        
        return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)

    # 🔹 DELETE: Soft delete user (mark inactive)
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = False  # Soft delete
        user.deleted_at = timezone.now()
        user.save()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class BranchView(APIView):
    # 🔹 GET: Retrieve all branches
    def get(self, request):
        branches = Branch.objects.filter(is_active=True)  # Get only active branches
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 POST: Create a new branch
    def post(self, request):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BranchDetailView(APIView):

    # 🔹 GET: Retrieve a single branch by ID
    def get(self, request, branch_id):
        branch = get_object_or_404(Branch, id=branch_id, is_active=True)
        serializer = BranchSerializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 PUT: Update a branch by ID
    def put(self, request, branch_id):
        branch = get_object_or_404(Branch, id=branch_id)
        serializer = BranchSerializer(branch, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 DELETE: Soft delete a branch (mark inactive)
    def delete(self, request, branch_id):
        branch = get_object_or_404(Branch, id=branch_id)
        branch.is_active = False  # Soft delete
        branch.deleted_at = timezone.now()
        branch.save()
        return Response({"message": "Branch deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class CustomerListCreateAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    """
    Handles listing all customers (GET) and creating a new customer (POST).
    """
    
    def get(self, request):
        q_data=request.query_params.get('data')
        if q_data=="customer_list":
            customers = Customer.objects.filter(deleted_at__isnull=True).values(
                'id', 'custom_id', 'name', 'mobile_number1','address1','address2', 'email'
            )
            return Response(customers, status=status.HTTP_200_OK)
        else:
            customers = Customer.objects.filter(deleted_at__isnull=True)
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)

    def post(self, request):
        user=request.user
        codename="add_customer"
        if has_permission(user.email,codename):
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"You have no permissions"},status=status.HTTP_404_NOT_FOUND)


class CustomerDetailAPIView(APIView):
    """
    Handles retrieving (GET), updating (PUT/PATCH), and soft deleting (DELETE) a single customer.
    """

    def get_object(self, customer_id):
        return get_object_or_404(Customer, id=customer_id, deleted_at__isnull=True)

    def get(self, request, customer_id):
        customer = self.get_object(customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, customer_id):
        customer = self.get_object(customer_id)
        serializer = CustomerSerializer(customer, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, customer_id):
        customer = self.get_object(customer_id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, customer_id):
        customer = self.get_object(customer_id)
        customer.deleted_at = timezone.now()
        customer.is_active = False
        customer.save()
        return Response({"message": "Customer soft deleted"}, status=status.HTTP_204_NO_CONTENT)
class ModelListCreateAPIView(APIView):
    def get(self, request):
        models = Model_data.objects.all()
        serializer = ModelDataSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ModelDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ModelDetailAPIView(APIView):
    def get_object(self, model_id):
        try:
            return Model_data.objects.get(id=model_id)
        except Model_data.DoesNotExist:
            return None

    def get(self, request, model_id):
        model = self.get_object(model_id)
        if model is None:
            return Response({"error": "ModelData not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer =ModelDataSerializer(model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, model_id):
        model = self.get_object(model_id)
        if model is None:
            return Response({"error": "ModelData not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ModelDataSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, model_id):
        model = self.get_object(model_id)
        if model is None:
            return Response({"error": "ModelData not found"}, status=status.HTTP_404_NOT_FOUND)
        model.delete()
        return Response({"message": "ModelData deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class MaterialDataListCreateAPIView(APIView):
    def get(self, request):
        material_data = MaterialData.objects.all()
        serializer = MaterialDataSerializer(material_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MaterialDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaterialDataDetailAPIView(APIView):
    def get_object(self, material_id):
        try:
            return MaterialData.objects.get(id=material_id)
        except MaterialData.DoesNotExist:
            return None

    def get(self, request, material_id):
        material_data = self.get_object(material_id)
        if material_data is None:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialDataSerializer(material_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, material_id):
        material_data = self.get_object(material_id)
        if material_data is None:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialDataSerializer(material_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, material_id):
        material_data = self.get_object(material_id)
        if material_data is None:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        material_data.delete()
        return Response({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class MaterialListCreateAPIView(APIView):
    def get(self, request):
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDetailAPIView(APIView):
    def get_object(self, material_id):
        try:
            return Material.objects.get(id=material_id)
        except Material.DoesNotExist:
            return None

    def get(self, request, material_id):
        material = self.get_object(material_id)
        if material is None:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialSerializer(material)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, material_id):
        material = self.get_object(material_id)
        if material is None:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, material_id):
        material = self.get_object(material_id)
        if material is None:
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        material.delete()
        return Response({"message": "Material deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class PrintTypeListCreateAPIView(APIView):
    def get(self, request):
        print_types = PrintType.objects.all()
        serializer = PrintTypeSerializer(print_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PrintTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrintTypeDetailAPIView(APIView):
    def get_object(self, print_type_id):
        try:
            return PrintType.objects.get(id=print_type_id)
        except PrintType.DoesNotExist:
            return None

    def get(self, request, print_type_id):
        print_type = self.get_object(print_type_id)
        if print_type is None:
            return Response({"error": "Print Type not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PrintTypeSerializer(print_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, print_type_id):
        print_type = self.get_object(print_type_id)
        if print_type is None:
            return Response({"error": "Print Type not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PrintTypeSerializer(print_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, print_type_id):
        print_type = self.get_object(print_type_id)
        if print_type is None:
            return Response({"error": "Print Type not found"}, status=status.HTTP_404_NOT_FOUND)
        print_type.delete()
        return Response({"message": "Print Type deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
class ItemView(APIView):
    def get(self, request):
        items = Item.objects.filter(is_active=True)  # Fetch only active items
        q_data=request.query_params.get('data')
        if q_data=="item_list":
            item_list = []
            for item in items:
                item_list.append({
                    "id": item.id,
                    "name": item.name,
                    "item_cost": float(item.item_cost),  # Convert Decimal to float
                    "material": item.material.name if item.material else None,  # Avoid NoneType error
                    "print_type": item.print_type.name if item.print_type else None,
                    "size": item.size,
                    "is_sleeve": item.is_sleeve,

                })

            return Response(item_list, status=status.HTTP_200_OK)
        
        # Apply pagination
        paginator = CustomPagination()
        paginated_items = paginator.paginate_queryset(items, request)
        item_list = []
        for item in paginated_items:
            item_list.append({
                "id": item.id,
                "name": item.name,
                "item_code": item.item_code,
                "item_cost": float(item.item_cost),  # Convert Decimal to float
                "item_alert": item.item_alert,
                "material": item.material.name if item.material else None,  # Avoid NoneType error
                "gst": float(item.gst) if item.gst else None,
                "tax": float(item.tax) if item.tax else None,
                "print_type": item.print_type.name if item.print_type else None,
                "size": item.size,
                "is_sleeve": item.is_sleeve,
                "item_description": item.item_description,
                "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else None,

            })

        return paginator.get_paginated_response(item_list)
    def post(self, request):
        try:
            # Extract fields from request data
            name = request.data.get("name")
            item_code = request.data.get("item_code")
            item_cost = request.data.get("item_cost")
            item_alert = request.data.get("item_alert")
            material_id = request.data.get("material")
            gst = request.data.get("gst")
            tax = request.data.get("tax")
            print_type_id = request.data.get("print_type")
            size = request.data.get("size")
            is_sleeve = request.data.get("is_sleeve")
            item_description = request.data.get("item_description")

            # Validate required fields
            if not all([name, item_code, item_cost, item_description]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Validate numeric fields
            try:
                item_cost = Decimal(item_cost)
                gst = Decimal(gst) if gst else None
                tax = Decimal(tax) if tax else None
            except:
                return Response({"error": "Invalid number format for cost, GST, or tax"}, status=status.HTTP_400_BAD_REQUEST)

            # Get related objects
            material = Material.objects.get(id=material_id) if material_id else None
            print_type = PrintType.objects.get(id=print_type_id) if print_type_id else None

            # Create the Item object
            item = Item.objects.create(
                name=name,
                item_code=item_code,
                item_cost=item_cost,
                item_alert=item_alert,
                material=material,
                gst=gst,
                tax=tax,
                print_type=print_type,
                size=size,
                is_sleeve=is_sleeve,
                item_description=item_description,
            )
            item.save()
            # Response data
            return Response({
                "message": "Item created successfully!"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class ItemDetailedView(APIView):
    def get(self, request, item_id=None):
        """Get a single item by ID or list all items if no ID is provided."""
        if item_id:
            item = get_object_or_404(Item, id=item_id, is_active=True)
            return Response({
                "id": item.id,
                "name": item.name,
                "item_code": item.item_code,
                "item_cost": float(item.item_cost),
                "item_alert": item.item_alert,
                "material": item.material.name if item.material else None,
                "gst": float(item.gst) if item.gst else None,
                "tax": float(item.tax) if item.tax else None,
                "print_type": item.print_type.name if item.print_type else None,
                "size": item.size,
                "is_sleeve": item.get_is_sleeve_display(),
                "item_description": item.item_description,
                "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }, status=status.HTTP_200_OK)
    def put(self, request, item_id):
        """Update an existing item."""
        item = get_object_or_404(Item, id=item_id, is_active=True)
        
        try:
            # Extract fields from request data
            item.name = request.data.get("name", item.name)
            item.item_code = request.data.get("item_code", item.item_code)
            item.item_alert = request.data.get("item_alert", item.item_alert)
            item.size = request.data.get("size", item.size)
            item.is_sleeve = request.data.get("is_sleeve", item.is_sleeve)
            item.item_description = request.data.get("item_description", item.item_description)

            # Handle optional decimal fields
            if "item_cost" in request.data:
                item.item_cost = Decimal(request.data["item_cost"])
            if "gst" in request.data:
                item.gst = Decimal(request.data["gst"]) if request.data["gst"] else None
            if "tax" in request.data:
                item.tax = Decimal(request.data["tax"]) if request.data["tax"] else None

            # Handle optional foreign keys
            if "material" in request.data:
                item.material = Material.objects.get(id=request.data["material"]) if request.data["material"] else None
            if "print_type" in request.data:
                item.print_type = PrintType.objects.get(id=request.data["print_type"]) if request.data["print_type"] else None

            item.save()

            return Response({
                "message": "Item updated successfully!",
                "id": item.id,
                "name": item.name,
                "item_code": item.item_code,
                "item_cost": float(item.item_cost),
                "item_alert": item.item_alert,
                "material": item.material.name if item.material else None,
                "gst": float(item.gst) if item.gst else None,
                "tax": float(item.tax) if item.tax else None,
                "print_type": item.print_type.name if item.print_type else None,
                "size": item.size,
                "is_sleeve": item.get_is_sleeve_display(),
                "item_description": item.item_description,
                "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        """Soft delete an item (mark it as inactive)."""
        item = get_object_or_404(Item, id=item_id, is_active=True)
        item.is_active = False
        item.save()

        return Response({"message": "Item deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
class UserRoleListCreateAPIView(APIView):
    """
    Handle GET (list all roles) and POST (create new role).
    """

    def get(self, request):
        roles = UserRole.objects.filter(is_active=True)  # Fetch only active roles
        serializer = UserRoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRoleDetailAPIView(APIView):
    """
    Handle GET by ID, PUT (update), and DELETE (soft delete).
    """

    def get_object(self, pk):
        return get_object_or_404(UserRole, pk=pk)

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = UserRoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        role = self.get_object(pk)
        serializer = UserRoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.deleted_at = timezone.now()  # Soft delete
        role.is_active = False
        role.save()
        return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)