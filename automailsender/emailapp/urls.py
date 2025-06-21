from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/', views.email_settings, name='email_settings'),
    path('send-email/', views.send_email, name='send_email'),
    path('bulk-email/', views.bulk_email, name='bulk_email'),
    path('logs/', views.email_logs, name='email_logs'),
]