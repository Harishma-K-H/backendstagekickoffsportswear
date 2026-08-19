from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Branch,User,Customer,Material,PrintType,Model_data,Item,UserRole,MaterialData,District,State
from .serializers import BranchSerializer,CustomTokenObtainPairSerializer,UserRoleSerializer,MaterialDataSerializer,UserSerializer,CustomerSerializer,StateSerializer,PrintTypeSerializer,MaterialSerializer,ModelDataSerializer
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
from .pagination import CustomPagination
from django.db.models import Q



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
    def get(self, request):
        q_data = request.query_params.get('data')
        print("🔍 Query Param:", q_data)  # Debug print

        branches = Branch.objects.filter(is_active=True)

        if q_data and q_data.lower() == "branch_list":
            data = [
                {
                    "id": branch.id,
                    "name": branch.name,
                    "code": branch.code
                }
                for branch in branches
            ]
            return Response(data, status=status.HTTP_200_OK)

        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 🔹 POST: Create a new branch
    def post(self, request):
        print("request.data",request.data)
        serializer = BranchSerializer(data=request.data)
        is_active=True
        if serializer.is_valid():
            serializer.save(is_active=is_active)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StateList(APIView):
    def get(self, request):
        states = State.objects.filter(is_active=True)
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        q_search=request.query_params.get('search')
        q_data=request.query_params.get('data')
        if q_data=="customer_list":
            customers = Customer.objects.filter(is_active=True).values(
                'id', 'custom_id', 'name', 'mobile_number1','address1','address2','address3', 'email','business_name','gst_no','mobile_number2','state__name'
            )
            if q_search:
                customers = customers.filter(
                    Q(custom_id__icontains=q_search) | 
                    Q(name__icontains=q_search) |
                    Q(business_name__icontains=q_search)| 
                    Q(gst_no__icontains=q_search)
                    )

            return Response(list(customers), status=status.HTTP_200_OK)
        else:
            customers = Customer.objects.all().order_by('-id')
            if q_search:
                customers = customers.filter(
                    Q(custom_id__icontains=q_search) | 
                    Q(name__icontains=q_search) |
                    Q(business_name__icontains=q_search)| 
                    Q(gst_no__icontains=q_search)
                    )
            paginator = CustomPagination()
            paginated_customer = paginator.paginate_queryset(customers, request)
            # customers = Customer.objects.filter(deleted_at__isnull=True)
            serializer = CustomerSerializer(paginated_customer, many=True)
            return paginator.get_paginated_response (serializer.data)

    def post(self, request):
        user=request.user
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     


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

        data = request.data

        try:
            customer.name = data.get('name', customer.name)
            customer.business_name = data.get('business_name', customer.business_name)
            customer.address1 = data.get('address1', customer.address1)
            customer.address2 = data.get('address2', customer.address2)
            customer.address3 = data.get('address3', customer.address3)
            customer.pincode = data.get('pincode', customer.pincode)
            customer.mobile_number1 = data.get('mobile_number1', customer.mobile_number1)
            customer.mobile_number2 = data.get('mobile_number2', customer.mobile_number2)
            customer.email = data.get('email', customer.email)
            customer.gst_no = data.get('gstn', customer.gst_no)

            # If you're sending state as ID
            if data.get('state'):
                customer.state_id = data['state']

            customer.save()
            # log_user_activity(request, f"Customer {customer.custom_id} updated successfully")

            return Response({
                "message": "Customer updated successfully",
                "customer_id": customer.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
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
        q_data = request.query_params.get('data')

        # If query param is "model_list", return only id and name
        if q_data == "model_list":
            model_list = list(Model_data.objects.values("id", "name"))  # Fetch only id and name
            return Response(model_list, status=status.HTTP_200_OK)

        # Otherwise, return all model data
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
        model_id = request.query_params.get('model_id')
        if model_id:
            try:
                model_id = int(model_id)  # Convert to int for correct filtering
                print_type_list = list(PrintType.objects.filter(model_id=model_id).values("id", "name"))
                return Response(print_type_list, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "Invalid model_id"}, status=status.HTTP_400_BAD_REQUEST)

        # If no model_id is passed, return all
        print_type_list = list(PrintType.objects.values("id", "name"))
        return Response(print_type_list, status=status.HTTP_200_OK)        

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
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        branch_search = request.query_params.get('branch_search')
        itemcode_search = request.query_params.get('itemcode_search')
        print_type_search = request.query_params.get('print_type_search')
        material_search = request.query_params.get('material_search')
        model_search = request.query_params.get('model_search')
        q_data = request.query_params.get('data')

        # Base queryset
        if user.role.name == "Admin":
            items = Item.objects.all().order_by('-created_at')
        else:
            items = Item.objects.filter(Q(created_by__branch=user.branch) |
                                        Q(branch=user.branch)
            ).order_by('-created_at')

        # Optional filtering
        if itemcode_search:
            items = items.filter(item_code__icontains=itemcode_search)
        if print_type_search:
            items = items.filter(print_type__name__icontains=print_type_search)
        if material_search:
            items = items.filter(material__name__icontains=material_search)
        if model_search:
            items = items.filter(model__id__icontains=model_search)
        if branch_search:
            items = items.filter(Q(created_by__branch__name__icontains=branch_search)|Q(branch__id=branch_search))

        # If just list (no pagination required)
        if q_data == "item_list":
            item_list = []
            for item in items:
                item_list.append({
                    "id": item.id,
                    "name": item.name,
                    "model_name": item.model.name if item.model else None,
                    "item_cost": float(item.item_cost),
                    "branch": {
                    'id': item.branch.id if item.branch else None,
                    'name': item.branch.name if item.branch else None,
                    'code': item.branch.code if item.branch else None
                    },
                    "material_id": item.material.id if item.material else None,
                    "material": item.material.name if item.material else None,
                    "print_type": item.print_type.name if item.print_type else None,
                    "size": item.size,
                    "is_sleeve": item.is_sleeve,
                    "is_active": item.is_active,
                })
            return Response(item_list, status=status.HTTP_200_OK)

        # Paginated item list
        paginator = CustomPagination()
        paginated_items = paginator.paginate_queryset(items, request)

        item_list = []
        for item in paginated_items:
            item_list.append({
                "id": item.id,
                "name": item.name,
                "model_name": item.model.name if item.model else None,
                "item_code": item.item_code,
                "item_cost": float(item.item_cost),
                "item_alert": item.item_alert,
                "material": item.material.id if item.material else None,
                "model": item.model.id if item.model else None,
                "print_type": item.print_type.id if item.print_type else None,
                "material_name": item.material.name if item.material else None,
                "gst": float(item.gst) if item.gst else None,
                "tax": float(item.tax) if item.tax else None,
                "print_type_name": item.print_type.name if item.print_type else None,
                "size": item.size,
                "HSN":item.HSN,
                "branch": {
                    'id': item.branch.id if item.branch else None,
                    'name': item.branch.name if item.branch else None,
                    'code': item.branch.code if item.branch else None
                },
                "sleevecase": item.is_sleeve,
                "item_description": item.item_description,
                "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S') if item.created_at else None,
                'is_active':item.is_active
            })

        return paginator.get_paginated_response(item_list)

    def post(self, request):
        try:
            q_data=request.query_params.get('data')
            branch = None
            user = request.user

            # Check for Admin user and branch ID
            if user.role.name == "Admin":
                branch_id = request.data.get('branch')
                if not branch_id:
                    return Response({"error": "Branch ID is required for Admin users."}, status=status.HTTP_400_BAD_REQUEST)
                branch = get_object_or_404(Branch, id=branch_id)
            else:
                branch = user.branch
            
            # Extract fields from request data
            name = request.data.get("name")
            item_code = request.data.get("item_code")
            item_cost = request.data.get("item_cost")
            item_alert = request.data.get("item_alert")
            model_id = request.data.get('model')
            material_id = request.data.get("material")
            gst = request.data.get("gst")
            tax = request.data.get("tax")
            print_type_id = request.data.get("print_type")
            size = request.data.get("size")
            is_sleeve = request.data.get("sleevecase")
            item_description = request.data.get("item_description")
            
            # Validate required fields
            if not all([name, item_cost]):
                return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

            # Validate numeric fields
            try:
                item_cost = Decimal(item_cost)
                gst = Decimal(gst) if gst else None
                tax = Decimal(tax) if tax else None
            except:
                return Response({"error": "Invalid number format for cost, GST, or tax"}, status=status.HTTP_400_BAD_REQUEST)
            # Get related objects
            model = Model_data.objects.get(id=model_id) if model_id else None 
            material = Material.objects.get(id=material_id) if material_id else None
            print_type = PrintType.objects.get(id=print_type_id) if print_type_id else None
            print_type_name=print_type.name
            # if q_data=="generate_itemcode":
            base_code = f"{name.strip()[:3].upper()}{print_type_name[0].upper()}"
            existing_codes = Item.objects.filter(item_code__startswith=base_code).values_list('item_code', flat=True)
            # Find max serial number
            serials = []
            for code in existing_codes:
                suffix = code.replace(base_code, "")
                if suffix.isdigit():
                    serials.append(int(suffix))
            next_serial = max(serials) + 1 if serials else 1
            item_code = f"{base_code}{str(next_serial).zfill(3)}"
            # Check if an item with the same name and other optional fields (material, print_type, is_sleeve) already exists in the same branch
            filter_kwargs = {
                'name': name,
                'branch': branch
            }

            # Add optional fields to the filter if they are provided
            if material:
                filter_kwargs['material'] = material
            if print_type:
                filter_kwargs['print_type'] = print_type
            if is_sleeve is not None:
                filter_kwargs['is_sleeve'] = is_sleeve

            existing_item = Item.objects.filter(**filter_kwargs).first()

            if existing_item:
                return Response({
                    "error": "Item with the same name already exists in this branch.",
                    "existing_item_id": existing_item.id,
                    "existing_item_code": existing_item.item_code
                }, status=status.HTTP_400_BAD_REQUEST)

            # Create the Item object
            item = Item.objects.create(
                name=name,
                model=model,
                item_code=item_code,
                item_cost=item_cost,
                item_alert=item_alert,
                material=material,
                gst=gst,
                tax=tax,
                branch=branch,
                print_type=print_type,
                size=size,
                is_sleeve=is_sleeve,
                item_description=item_description,
            )
            item.save()

            # Response data
            return Response({
                "message": "Item created successfully!",
                "item_id": item.id,
                "item_code": item.item_code
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class ItemDetailedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_item(self, request, item_id):
        """Return an active item that the requesting user is allowed to access."""
        queryset = Item.objects.filter(is_active=True)
        role_name = getattr(getattr(request.user, "role", None), "name", None)
        if role_name != "Admin":
            if request.user.branch_id is None:
                raise PermissionDenied("Your user account is not assigned to a branch.")
            queryset = queryset.filter(
                Q(branch=request.user.branch) |
                Q(created_by__branch=request.user.branch)
            )
        return get_object_or_404(queryset, id=item_id)

    def get(self, request, item_id=None):
        """Get a single item by ID or list all items if no ID is provided."""
        if item_id:
            item = self.get_item(request, item_id)
            return Response({
                "id": item.id,
                "name": item.name if item.name else None,
                "model": item.model.name if item.model else None,
                "item_code": item.item_code,
                "item_cost": float(item.item_cost),
                "item_alert": item.item_alert,
                "material": item.material.name if item.material else None,
                "gst": float(item.gst) if item.gst else None,
                "tax": float(item.tax) if item.tax else None,
                "print_type": item.print_type.name if item.print_type else None,
                "size": item.size,
                "branch": {
                    'id': item.branch.id if item.branch else None,
                    'name': item.branch.name if item.branch else None,
                    'code': item.branch.code if item.branch else None
                },
                "is_sleeve": item.get_is_sleeve_display(),
                "item_description": item.item_description,
                "created_at": item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }, status=status.HTTP_200_OK)
    def put(self, request, item_id):
        """Update an existing item."""
        item = self.get_item(request, item_id)

        try:
            # Extract updated fields
            name = request.data.get("name", item.name)
            item_code = request.data.get("item_code", item.item_code)
            item_alert = request.data.get("item_alert", item.item_alert)
            size = request.data.get("size", item.size)
            is_sleeve = request.data.get(
                "is_sleeve", request.data.get("sleevecase", item.is_sleeve)
            )
            item_description = request.data.get("item_description", item.item_description)
            branch = item.branch
            if "branch" in request.data:
                role_name = getattr(getattr(request.user, "role", None), "name", None)
                if role_name != "Admin":
                    raise PermissionDenied("Only an Admin can move an item to another branch.")
                branch_id = request.data.get("branch")
                branch = Branch.objects.get(id=branch_id) if branch_id else None

            item_cost = item.item_cost
            if "price" in request.data or "item_cost" in request.data:
                price = request.data.get("price", request.data.get("item_cost"))
                item_cost = Decimal(price)

            gst = item.gst
            if "gst" in request.data:
                gst = Decimal(request.data["gst"]) if request.data["gst"] else None

            tax = item.tax
            if "tax" in request.data:
                tax = Decimal(request.data["tax"]) if request.data["tax"] else None

            # Related fields
            model = item.model
            if "model" in request.data:
                model = Model_data.objects.get(id=request.data["model"]) if request.data["model"] else None

            material = item.material
            if "material" in request.data:
                material = Material.objects.get(id=request.data["material"]) if request.data["material"] else None
            print_type = item.print_type
            if "printType" in request.data:
                print_type = PrintType.objects.get(id=request.data["printType"]) if request.data["printType"] else None

            # Check for duplicates in the same branch
            duplicate_qs = Item.objects.filter(
                branch=item.branch,
                model=model,
                material=material,
                print_type=print_type,
                is_sleeve=is_sleeve
            ).exclude(id=item.id)

            if duplicate_qs.exists():
                duplicate_item = duplicate_qs.first()  # ✅ valid now
                return Response({
                    "error": "Item with the same model, material, print type, and sleeve option already exists in this branch.",
                    "existing_item_id": duplicate_item.id,
                    "existing_item_name": duplicate_item.name,
                }, status=status.HTTP_400_BAD_REQUEST)

            # Apply updates
            item.name = name
            item.item_code = item_code
            item.item_alert = item_alert
            item.size = size
            item.is_sleeve = is_sleeve
            item.item_description = item_description
            item.item_cost = item_cost
            item.gst = gst
            item.branch=branch
            item.tax = tax
            item.model = model
            item.material = material
            item.print_type = print_type

            item.save()

            return Response({
                "message": "Item updated successfully!",
                "id": item.id,
                "name": item.name,
                "item_code": item.item_code,
                "item_cost": float(item.item_cost),
                "item_alert": item.item_alert,
                "model": item.model.name if item.model else None,
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
        item = self.get_item(request, item_id)
        item.is_active = False
        item.save()

        return Response({"message": "Item deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


class ItemStatusView(APIView):
    """Change only an item's active status without touching catalog fields."""

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, item_id):
        role_name = getattr(getattr(request.user, "role", None), "name", None)
        if role_name != "Admin":
            raise PermissionDenied("Only an Admin can change item status.")

        if "is_active" not in request.data or not isinstance(request.data["is_active"], bool):
            return Response(
                {"error": "is_active must be a boolean."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item = get_object_or_404(Item.objects.all(), id=item_id)
        item.is_active = request.data["is_active"]
        item.save(update_fields=["is_active"])
        return Response(
            {
                "message": "Item status updated successfully!",
                "id": item.id,
                "is_active": item.is_active,
            },
            status=status.HTTP_200_OK,
        )
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
    
class ModelMaterialList(APIView):
    def get(self, request, model_id):
        material=Material.objects.filter(model_id=model_id)
        material_names = list(material.values('id','name','model_id'))
        if not material_names:
            return Response({"error": "No materials found for this model."}, status=status.HTTP_404_NOT_FOUND)
        return Response(material_names, status=status.HTTP_200_OK)

class ItemCostView(APIView):
    def get(self, request):
        model = request.query_params.get('model')
        material = request.query_params.get('material')
        print_type = request.query_params.get('print_type')
        sleeve_case = request.query_params.get('sleevecase')
        branch = request.user.branch

        print(f"🔍 Received Params - Model: {model}, Material: {material}, PrintType: {print_type}, SleeveCase: {sleeve_case}")

        # Basic checks for required fields
        if not Item.objects.filter(model=model).exists():
            return Response({"error": "Model not found in database"}, status=status.HTTP_400_BAD_REQUEST)

        if not Item.objects.filter(print_type_id=print_type).exists():
            return Response({"error": "Print type not found in database"}, status=status.HTTP_400_BAD_REQUEST)

        if not Item.objects.filter(branch=branch).exists():
            return Response({"error": "Branch not found in database"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare filter criteria
        filter_criteria = {
            "model": model,
            "print_type_id": print_type,
            "branch": branch
        }

        # Handle the 'material' parameter (ensure it's valid)
        if material and material.lower() not in ['undefined', 'null', '']:
            if not Item.objects.filter(material_id=material).exists():
                return Response({"error": "Material not found in database"}, status=status.HTTP_400_BAD_REQUEST)
            filter_criteria["material_id"] = material

        # Handle the 'sleevecase' parameter (optional)
        if sleeve_case and sleeve_case.lower() not in ['undefined', 'null', '']:
            filter_criteria["is_sleeve"] = sleeve_case

        print(f"🔍 Filter Criteria: {filter_criteria}")

        # Fetch the item
        item = Item.objects.filter(**filter_criteria).first()

        if not item:
            return Response({"error": "Model not match"}, status=status.HTTP_404_NOT_FOUND)

        item_data = {
            "id": item.id,
            "name": item.name,
            "cost": item.item_cost,
            "item_code": item.item_code
        }

        return Response(item_data, status=status.HTTP_200_OK)
