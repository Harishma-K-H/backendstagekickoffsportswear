from django.urls import path
from .views import DetailedOrderAPIView,CreateOrderAPIView,GetNextOrderNumberAPIView,OrderPaymentAPI,OrderPaymentDetails,OrderItemUpdateView,InvoiceList,InvoiceView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api_order/',CreateOrderAPIView.as_view(),name='orders_list'),
    path('update-order-item/', OrderItemUpdateView.as_view(), name='update-order-item'),
    path('order/details/<int:order_id>/',DetailedOrderAPIView.as_view(),name='order_list'),
    path("order_no_generate/", GetNextOrderNumberAPIView.as_view(), name="order_numbers"),
    path('api/payment/',OrderPaymentAPI.as_view(),name='order_payment'),
    path('invoice_list/',InvoiceList.as_view(),name='invoice_list'),
    path('invoices/<str:invoice_id>/', InvoiceView.as_view(), name='invoice-detail'),
    # path("invoice_no_generate/", GetInvoiceNumberAPIView.as_view(), name="invoice_number"),
    path('payment_details/<int:order_id>/',OrderPaymentDetails.as_view(),name='order_payment_details')
  


]