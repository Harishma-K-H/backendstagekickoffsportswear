from rest_framework import serializers
from .models import Branch,User,Customer,Item,UserRole,PrintType,Material,Menu,MenuAccess,Model_data,MaterialData
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password,check_password
from .permissions import has_permission
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.db.models import Q

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'  # Include all fields from the Branch model

class ModelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model_data
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
class MaterialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialData
        fields = '__all__'


class PrintTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintType
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__' 
    def validate_email(self, value):
        """
        Check if the email already exists in the database.
        """
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use. Please use a different email.")
        return value
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    login_identifier = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('email', None)  # Remove email field since we use login_identifier

    def validate(self, attrs):
        login_identifier = attrs.get('login_identifier')
        password = attrs.get('password')
        
        user = None  # Initialize user to avoid UnboundLocalError
        try:
            user = User.objects.get(
                Q(email=login_identifier) |
                Q(username=login_identifier) |
                Q(mobile_number__icontains=login_identifier)
            )
        except User.DoesNotExist:
            raise AuthenticationFailed({'error': 'Invalid Credentials!'})
        except Exception as e:
            print("Exception:", e)

        if not user:
            raise AuthenticationFailed({'error': 'Invalid Credentials!'})

        if not user.is_active:
            raise AuthenticationFailed({'error': 'Account is not active.'})

        refresh = self.get_token(user)
        try:
            data = {
                'status_code': status.HTTP_200_OK,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role.name if user.role else None,
                'name': user.get_full_name(),
                'branch_id': user.branch_id,
            }

            if user.role.name == 'Admin':
                # data['Desig'] = 'Admin'
                menu_data = self.get_all_menus()
            else:
                # data['Desig'] = user.designation.name if user.designation else "Unknown"
                menu_data = self.generate_menu_data(user.role)
            
            data['menus'] = menu_data
            return data
        except Exception as e:
            raise AuthenticationFailed({'error': str(e)})

    def get_admin_menu_data(self, menu):
        data = {
            'id': menu.id,
            'name': menu.name,
            'url': menu.url,
            'permissions': [{'id': permission.id, 'codename': permission.codename} for permission in menu.permissions.all()],
            'level': menu.level,
            # 'is_active': menu.is_active,
            # 'menu_icon_path': menu.menu_icon_path,
            'order': menu.order,
            'submenus': []
        }
        for submenu in menu.submenus.filter().order_by('order'):
            submenu_data = self.get_admin_menu_data(submenu)
            data['submenus'].append(submenu_data)
        return data

    def get_all_menus(self):
        menu_data = []
        menus = Menu.objects.filter(parent=None).prefetch_related('permissions', 'submenus').order_by('order')
        for menu in menus:
            menu_data.append(self.get_admin_menu_data(menu))
        return menu_data
    
    def generate_menu_data(self, user_role):
        menu_data = [{
            "id": 3,
            "name": "Dashboard",
            "url": "/",
            "level": "1",
            "menu_icon_path": "fa fa-home",
            "submenus": []
        }]
        
        menus = Menu.objects.filter(parent=None).exclude(name="Settings").prefetch_related('permissions', 'submenus').order_by('order')
        for menu in menus:
            if menu.permissions.filter(userrole=user_role).exists():
                parent_menu_entry = {
                    'id': menu.id,
                    'name': menu.name,
                    'url': menu.url,
                    'permissions': [{'id': permission.id, 'codename': permission.codename} for permission in menu.permissions.filter(userrole=user_role)],
                    'level': menu.level,
                    # 'is_active': menu.is_active,
                    # 'menu_icon_path': menu.menu_icon_path,
                    'submenus': self.get_submenu_data(menu, user_role),
                }
                menu_data.append(parent_menu_entry)
        return menu_data

    def get_submenu_data(self, menu, user_role):
        submenu_data = []
        for submenu in menu.submenus.filter().order_by('order'):
            if submenu.permissions.filter(userrole=user_role).exists():
                submenu_data.append({
                    'id': submenu.id,
                    'name': submenu.name,
                    'url': submenu.url,
                    'permissions': [{'id': permission.id, 'codename': permission.codename} for permission in submenu.permissions.filter(userrole=user_role)],
                    'level': submenu.level,
                    # 'is_active': submenu.is_active,
                    # 'menu_icon_path': submenu.menu_icon_path,
                    'submenus': self.get_submenu_data(submenu, user_role),
                })
        return submenu_data
class UserSerializer(serializers.ModelSerializer):
    branch=serializers.SerializerMethodField()
    role=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username','email','branch','role']
    def get_branch(self,obj):
        branch_id=obj.branch
        if branch_id:
            return {
                'id':branch_id.id,
                'name':branch_id.name,
                'code':branch_id.code,
                'location':branch_id.location
            }
        else:
            return None
    def get_role(self,obj):
        role_id=obj.role
        if role_id:
            return{
                'id':role_id.id,
                'name':role_id.name
                }
        else:
            return None

    def create(self, validated_data):
        # Extract role from validated data if provided
        role_data = validated_data.pop('role', None)

        if role_data:
            try:
                role = UserRole.objects.get(id=role_data.id)  # Fetch role by ID
            except UserRole.DoesNotExist:
                raise serializers.ValidationError({"role": "Invalid role ID provided."})
        else:
            role = UserRole.objects.get(id=2)  # Default to 'User' role

        user = User.objects.create(**validated_data, role=role)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'item_code', 'item_cost']