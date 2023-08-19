from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FloatUrlParameterConverter, "float")

urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_detail/<str:order_number>/', views.order_detail, name='order_detail'),
    
]
