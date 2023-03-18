from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.payments, name='payments'),
    path('place_order/<int:total>/<int:quantity>/', views.place_order, name='place_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
