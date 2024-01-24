from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from service.models import Service
from .serializers import ServiceSerializer 
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


@api_view(['GET'])
def get_all_services(request):
    services= Service.objects.all()
    serializer = ServiceSerializer(services,many=True)
    print(services)
    return Response({"service":serializer.data})
