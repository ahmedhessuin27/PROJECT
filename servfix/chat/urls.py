from django.urls import path
from .views import *

urlpatterns = [
    path('api/messages/', message_list, name='message-list'),
    path('api/messages/<int:pk>/', message_delete, name='message-delete'),
]






'''
from django.contrib.auth.models import User

# Check if a user with ID 1 exists
user1_exists = User.objects.filter(id=1).exists()
print("User with ID 1 exists:", user1_exists)

# Check if a user with ID 2 exists
user2_exists = User.objects.filter(id=2).exists()
print("User with ID 2 exists:", user2_exists)

'''