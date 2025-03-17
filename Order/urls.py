from django.urls import path
from .views import DetailedOrderAPIView,CreateOrderAPIView,GetNextOrderNumberAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api_order/',CreateOrderAPIView.as_view(),name='orders_list'),
    path('order/details/<int:order_id>/',DetailedOrderAPIView.as_view(),name='order_list'),
    path("order_no_generate/", GetNextOrderNumberAPIView.as_view(), name="order_numbers")
]