from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FloatUrlParameterConverter, "float")

urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('place_order/', views.place_order, name='place_order'),
    path('refund/',views.refund,name='refund')
]
