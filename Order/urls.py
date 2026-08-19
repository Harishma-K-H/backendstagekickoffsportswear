from django.urls import path
from .views import DetailedOrderAPIView,CreateOrderAPIView,GetNextOrderNumberAPIView,OrderPaymentAPI,OrderPaymentDetails,OrderItemUpdateView,InvoiceList,InvoiceView,CustomerDetails,OrderByDeliveryDateAPIView,InvoiceReportAPI,CanceledOrdersAPI
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/api_order/',CreateOrderAPIView.as_view(),name='orders_list'),
    path('api/update-order-item/', OrderItemUpdateView.as_view(), name='update-order-item'),
    path('api/order/details/<int:order_id>/',DetailedOrderAPIView.as_view(),name='order_list'),
    path("api/order_no_generate/", GetNextOrderNumberAPIView.as_view(), name="order_numbers"),
    path('api/payment/',OrderPaymentAPI.as_view(),name='order_payment'),
    path('api/invoice_list/',InvoiceList.as_view(),name='invoice_list'),
    path('api/invoices/<int:invoice_id>/', InvoiceView.as_view(), name='invoice-detail'),
    # path("invoice_no_generate/", GetInvoiceNumberAPIView.as_view(), name="invoice_number"),
    path('api/payment_details/<int:order_id>/',OrderPaymentDetails.as_view(),name='order_payment_details'),
    path('api/customer_details/<int:pk>/',CustomerDetails.as_view(),name="customer_details"),
    path('api/orders-by-date/', OrderByDeliveryDateAPIView.as_view(), name='orders-by-date'),
    path('api/invoice_reports/',InvoiceReportAPI.as_view(),name='invoice_report'),
    path('api/canceledorders/<int:order_id>/',CanceledOrdersAPI.as_view(),name="cancel-orders")
  


]
