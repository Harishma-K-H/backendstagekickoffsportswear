from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Branch,User,Item,Customer,CustomUserManager,UserRole,PrintType,Material,Model_data,Menu,MenuAccess,MaterialData,District
# Register your models here.
admin.site.register(Branch)
admin.site.register(Item)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(UserRole)
admin.site.register(PrintType)
admin.site.register(Material)
admin.site.register(Model_data)
admin.site.register(Menu)
admin.site.register(MenuAccess)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(MaterialData)
admin.site.register(District)