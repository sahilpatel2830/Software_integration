from django.urls import path
from .views import (EmployeeCreateView, QuickBooksInvoiceCreateView, QuickBooksCustomerCreateView,
                     QuickBookTimeActivity)

urlpatterns = [
    path('create-employee/', EmployeeCreateView.as_view(), name='employee-create'),
    path('create-invoice/', QuickBooksInvoiceCreateView.as_view(), name='invoice-create'),
    path('create-customer/', QuickBooksCustomerCreateView.as_view(), name='customer-create'),
    path('create-timeactivity/', QuickBookTimeActivity.as_view(), name='timeactivity-create')
]
