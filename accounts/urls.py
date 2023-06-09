from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.do_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot_password/', views.forgotPassword, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset_password/', views.resetPassword, name='reset_password'),
    path('setting/',views.setting,name='setting')
]
