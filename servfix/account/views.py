from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer,UserSerializer,ProviderSignUpSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from account.models import Userprofile,Providerprofile


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data = data)
    if user.is_valid():
        if not Userprofile.objects.filter(email=data['email']).exists():
             user=User.objects.create(
                   email=data['email'],
                   password=make_password(data['password']),
                   username=data['username'],
             )
             Userprofile.objects.create(
                user=user,
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
    
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user =SignUpSerializer(request.user,many=False)
    return Response(user.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    
    # user.username = data['username']
    user.email = data['email']
    user.phone = data['phone']
    user.address = data['address']
    user.city = data['city']

    if data['password'] !="":
        user.password = make_password(data['password'])
        
    user.save()
    serializer = UserSerializer(user,many=False)
    return Response(serializer.data)  
  
def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)



@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    
    host = get_current_host(request)
    link = "http://127.0.0.1:8000/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "Paswword reset from servfix",
        body,
        "servix@gmail.com",
        [data['email']]
    )
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})

 


@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None 
    user.profile.save() 
    user.save()
    return Response({'details': 'Password reset done '})
  



@api_view(['POST'])
def provider_register(request):
    data = request.data
    user = ProviderSignUpSerializer(data = data)
    if user.is_valid():
        if not Providerprofile.objects.filter(email=data['email']).exists() and not Providerprofile.objects.filter(username=data['username']).exists() :
             user=User.objects.create(
                   email=data['email'],
                   password=make_password(data['password']),
                   username=data['username'],
             )
             Providerprofile.objects.create(
                user=user,
                email=data['email'],
                username=data['username'],
                password=make_password(data['password']),
                address=data['address'],
                phone=data['phone'],
                city=data['city'],
                profession=data['profession'],
                fixed_salary=data['fixed_salary'],
                id_image=data['id_image'],
            )
             return Response(
                {'details':'Your account registered susccessfully!' },
                    status=status.HTTP_201_CREATED
                    )
        else:
            return Response(
                {'eroor':'This email or username already exists!' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
    else:
        return Response(user.errors)