from django.contrib import admin
from django.urls import path
from main_app import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('auth-token/', obtain_auth_token, name='auth_token'),
    path('admin/', admin.site.urls),
    path('messages/', views.list_all_messages),
    path('messages/unread', views.list_unread_messages),
    path('messages/new/<int:receiver_id>', views.create_message),
    path('messages/read/<int:message_id>/', views.read_message),
    path('messages/delete/<int:message_id>/', views.delete_message),
    ]