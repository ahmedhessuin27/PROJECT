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
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


@api_view(['GET'])
def get_all_services(request):
    services= Service.objects.all()
    serializer = ServiceSerializer(services,many=True)
    print(services)
    return Response({"service":serializer.data})
# create_service
@api_view(['POST'])
def create_service(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE service
@api_view(['DELETE'])
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()

    return Response({'detail': 'Service deleted sucessfully.'}, status=status.HTTP_204_NO_CONTENT)
