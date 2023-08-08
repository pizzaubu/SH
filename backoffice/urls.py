from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='backoffice_login'),
    path('logout/', views.logout, name='backoffice_logout'),
    path('order_detail/<str:order_number>/', views.order_detail, name='backoffice_order'),
    path('update_order_status/<str:status>/<int:order_id>',views.update_order_status, name='update_order_status'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<str:choices>/<int:product_id>', views.edit_product, name='edit_product'),
    path('edit_category/<str:edit>/<int:category_id>', views.edit_category, name='edit_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('update_payment_status/<str:status>/<int:payment_id>/<int:order_id>/', views.update_payment_status, name='update_payment_status'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard')

]