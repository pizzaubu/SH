from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.do_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reset_password/', views.resetPassword, name='reset_password'),
    path('forgot_password/',views.forgotPassword, name='forgot_password'),
    path('setting/',views.setting,name='setting')
]
