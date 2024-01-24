from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SingUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from account.models import Userprofile


@api_view(['POST'])
def register(request):
    data = request.data
    user = SingUpSerializer(data = data)

    if user.is_valid():
        if not Userprofile.objects.filter(email=data['email']).exists():
            user = Userprofile.objects.create(
                email=data['email'],
                username=data['username'],
                password=make_password(data['password']),
                address=data['address'],
                phone=data['phone'],
                city=data['city'],
            )
            return Response(
                {'details':'Your account registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user.errors)