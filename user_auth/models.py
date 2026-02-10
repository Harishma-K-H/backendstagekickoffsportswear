from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission,PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password,check_password
import string
import os
import random
from django.utils import timezone

class District(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class State(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    GSTIN=models.CharField(max_length=255,null=True,blank=True)
    code=models.CharField(max_length=255,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, unique=True)
    pincode=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,default="KERALA")
    email=models.CharField(max_length=100,null=True,blank=True)
    phn_no=models.CharField(max_length=12,null=True,blank=True)
    GSTN=models.CharField(max_length=100,default="GST01020")
    location = models.TextField(null=True,blank=True)
    remark = models.TextField(null=True,blank=True)
    account_details = models.TextField(null=True,blank=True)
    qr_code = models.FileField(upload_to='qr_codes/', null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    district=models.CharField(max_length=255,null=True,blank=True)
    city=models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo=models.FileField(upload_to="logos",null=True,blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('E-mail is Required')
        if not username:
            raise ValueError('Username is Required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Fetch or create the "Admin" role
        admin_role, created = UserRole.objects.get_or_create(name="Admin")

        # Set the role to Admin
        extra_fields.setdefault('role', admin_role)
        return self.create_user(email, username, password=password, **extra_fields)


def get_pro_pic_upload_path(instance, filename):
    date_str = timezone.now().strftime("%Y-%m-%d_%H%M%S")
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    ext = os.path.splitext(filename)[1]
    return f'profile_pic/{date_str}_{rand_str}{ext}'


class User(AbstractUser):
    emp_code = models.CharField(max_length=25, null=True, blank=True)
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, null=True, blank=True)
    last_name = models.CharField(max_length=35)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=35, null=True, blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    mobile_number = models.CharField(max_length=15, unique=True,null=True,blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    pro_pic = models.FileField(upload_to=get_pro_pic_upload_path, blank=True, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
 
    # Fix reverse accessor clashes
    # groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # it is command when create the super user
    # def save(self, *args, **kwargs):
    #     """ Ensure password is always hashed before saving """
    #     if self.pk:  # If updating an existing user
    #         existing_user = User.objects.filter(pk=self.pk).first()
    #         if existing_user and existing_user.password != self.password:
    #             self.password = make_password(self.password)  # Hash new password
    #     else:
    #         self.password = make_password(self.password)  # Hash password for new users
    #     super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     """ Ensure password is hashed only if it is not already hashed """
    #     if self.pk:  # If updating an existing user
    #         existing_user = User.objects.filter(pk=self.pk).first()
    #         if existing_user and not check_password(self.password, existing_user.password):
    #             self.password = make_password(self.password)  # Hash new password
    #     else:  # New user case
    #         self.password = make_password(self.password)  # Hash password for new users

    #     super().save(*args, **kwargs)
    def get_full_name(self):
        """
        Returns the full name by concatenating first name, middle name (if exists), and last name.
        """
        name_parts = [self.first_name, self.middle_name, self.last_name]  # Create a list of name parts
        return " ".join(filter(None, name_parts))  # Filter out None values and join with a space

    def __str__(self):
        return self.get_full_name()  # Return full name when printing the object
    def __str__(self):
        return self.email
class Customer(models.Model):
    custom_id= models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    business_name=models.CharField(max_length=255,null=True,blank=True)
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    address3= models.TextField(blank=True, null=True)
    pincode=models.CharField(max_length=100,null=True,blank=True)
    mobile_number1 = models.CharField(max_length=15, unique=True)
    mobile_number2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="created_by_customer")
    branch = models.ManyToManyField(
    Branch,
    blank=True,
    related_name="customers"
)
    def save(self, *args, **kwargs):
        if not self.custom_id:  # Generate only if not already set
            self.custom_id = self.generate_unique_custom_id()
        super().save(*args, **kwargs)

    def generate_unique_custom_id(self):
        while True:
            prefix = random.choice(string.ascii_uppercase)  # Random uppercase letter (A-Z)
            numeric_part = str(random.randint(1000000000, 9999999999))  # 10-digit number
            new_id = prefix + numeric_part  # Combine letter + number
            
            if not Customer.objects.filter(custom_id=new_id).exists():
                return new_id

    def __str__(self):
        return self.business_name

class ShippingCustomer(models.Model):
    custom_id= models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True,related_name="customer_shipment")
    name = models.CharField(max_length=255,null=True,blank=True)
    business_name=models.CharField(max_length=255,null=True,blank=True)
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    mobile_number1 = models.CharField(max_length=15, null=True,blank=True)
    mobile_number2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="created_by_shipment_customer")
    # def save(self, *args, **kwargs):
    #     if not self.custom_id:  # Generate only if not already set
    #         self.custom_id = self.generate_unique_custom_id()
    #     super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Model_data(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class MaterialData(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        model_name = self.name
        return model_name
class Material(models.Model):
    name = models.CharField(max_length=255)
    model_id=models.ForeignKey(Model_data,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        model_name = self.model_id.name if self.model_id else "No Model"
        return f"{self.name} ({model_name})"

    
class PrintType(models.Model):
    name = models.CharField(max_length=255)
    model=models.ForeignKey(Model_data,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.name} - {self.model.name if self.model else 'No Model'}"



class Item(models.Model):
    SLEEVE_CHOICES = [
        ('FULL SLEEVE', 'FULL SLEEVE'),
        ('SLEEVELESS', 'SLEEVELESS'),
        ('HALF SLEEVE', 'HALF SLEEVE'),
    ]

    name = models.CharField(max_length=255,null=True,blank=True)
    item_code = models.CharField(max_length=100,null=True,blank=True)
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)
    item_alert = models.IntegerField(null=True, blank=True)
    model=models.ForeignKey(Model_data, on_delete=models.CASCADE,null=True,blank=True)
    material = models.ForeignKey(Material,on_delete=models.CASCADE,null=True, blank=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    print_type = models.ForeignKey(PrintType,on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    HSN=models.CharField(max_length=20,null=True,blank=True,default="610990")
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True,related_name="item_branch")
    is_sleeve = models.CharField(max_length=20, choices=SLEEVE_CHOICES, null=True,blank=True)

    item_description = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="created_by_item")

    def __str__(self):
        return f"{self.id} - {self.name} ({self.get_is_sleeve_display()})"
    

class Menu(models.Model):
    name=models.CharField(max_length=255, null=True, blank=True)
    url= models.CharField(max_length=255, null=True, blank=True)
    icon= models.CharField(max_length=255, null=True, blank=True)
    order=models.IntegerField(null=True,blank=True)
    level = models.CharField(max_length=50,null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='submenus')
    permissions = models.ManyToManyField(Permission, blank=True)
    def __str__(self):
        return self.name

class MenuAccess(models.Model):
    """
    Defines which users can access specific menus and what actions they can perform.
    """
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=255, null=True, blank=True)
    url= models.CharField(max_length=255, null=True, blank=True)
    icon= models.CharField(max_length=255, null=True, blank=True)
    order=models.IntegerField(null=True,blank=True)
    level = models.CharField(max_length=50,null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    def __str__(self):
        return f"{self.user.email} - {self.menu.name}"


