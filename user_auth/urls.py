from django.urls import path
from .views import BranchView,login_view,BranchDetailView,UserView,UserDetailView,CustomerDetailAPIView,CustomerListCreateAPIView,MaterialListCreateAPIView,PrintTypeListCreateAPIView,MaterialDetailAPIView,PrintTypeDetailAPIView,ModelListCreateAPIView,ModelDetailAPIView,ItemView,ItemDetailedView,UserRoleListCreateAPIView,UserRoleDetailAPIView,MaterialDataListCreateAPIView,MaterialDataDetailAPIView,DistrictList,ModelMaterialList,ItemCostView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api_branch/',BranchView.as_view(),name='branch_list'),
    path('api_branch/details/<int:branch_id>/',BranchDetailView.as_view(),name='branch_list'),
    path("api/token/", login_view.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('district_list/',DistrictList.as_view(),name='district_list'),
    path('api/users/', UserView.as_view(), name='user_list'),  # GET all & POST new user
    path('api/users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),  # GET, PUT, DELETE user
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:customer_id>/', CustomerDetailAPIView.as_view(), name='customer-detail'),
    
    
    path('api/user_role/', UserRoleListCreateAPIView.as_view(), name='role-list-create'),
    path('api/user_role/<int:role_id>/', UserRoleDetailAPIView.as_view(), name='role-detail'),
    path('api/models/', ModelListCreateAPIView.as_view(), name='model-list-create'),
    path('api/models/<int:model_id>/', ModelDetailAPIView.as_view(), name='model-detail'),
    path('api/materials/', MaterialListCreateAPIView.as_view(), name='material-list-create'),
    path('api/materials/<int:material_id>/', MaterialDetailAPIView.as_view(), name='material-detail'),

    path('api/material_data/', MaterialDataListCreateAPIView.as_view(), name='material-list-create'),
    path('material_list/<int:model_id>/',ModelMaterialList.as_view(),name="model_material"),
    path('api/material_data/<int:material_id>/', MaterialDataDetailAPIView.as_view(), name='material-detail'),
    path('api/print-types/', PrintTypeListCreateAPIView.as_view(), name='print-type-list-create'),
    path('api/print-types/<int:print_type_id>/', PrintTypeDetailAPIView.as_view(), name='print-type-detail'),
    path('api_item/',ItemView.as_view(),name='item_list'),
    path('api_item/<int:item_id>/',ItemDetailedView.as_view(),name='item_detailed_list'),
    path('itemcost/',ItemCostView.as_view(),name="item_cost")
    
    
]

