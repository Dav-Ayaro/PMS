from django.urls import path
from . import views

urlpatterns = [
    path('invoice/create/', views.create_invoice, name='create_invoice'),
    path('payment/<int:invoice_id>/', views.record_payment, name='record_payment'),
]