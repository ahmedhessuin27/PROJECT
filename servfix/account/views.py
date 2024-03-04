from django.db.models import Avg
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer,UserSerializer,ProviderSignUpSerializer,ProviderSerializer,GetprovidersSerializer , GetallFavourites
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from account.models import Userprofile,Providerprofile , Review
from service.models import Service  
from .filtters import ProvidersFilter
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash





@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data = data)
    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists():
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
    profile = Userprofile.objects.get(user=request.user)
    serializer = UserSerializer(profile)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    profile = Userprofile.objects.get(user=request.user)
    user = request.user
    data = request.data
    
    user.username = data['username']
    profile.username = data['username']
    user.email = data['email']
    profile.email = data['email']
    profile.phone = data['phone']
    profile.address = data['address']
    profile.city = data['city']
    profile.image = data['image']

    if data['password'] !="":
        user.password = make_password(data['password'])
    
    if data['password'] !="":
        profile.password = make_password(data['password'])    
        
    user.save()
    profile.save()
    serializer = UserSerializer(profile)
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
    serv= Service.objects.get(name=data['profession'])

    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists() :
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
                service_id=serv,
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



@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def current_provider(request):
    profile = Providerprofile.objects.get(user=request.user)
    serializer = ProviderSerializer(profile)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_provider(request):
    profile = Providerprofile.objects.get(user=request.user)
    user = request.user
    data = request.data 
    user.username = data['username']
    profile.username = data['username']
    user.email = data['email']
    profile.email = data['email']
    profile.phone = data['phone']
    profile.address = data['address']
    profile.city = data['city']
    profile.profession = data['profession']
    profile.fixed_salary = data['fixed_salary']
    profile.image = data['image']
    
    if data['password'] != "":
        profile.password = make_password(data['password'])
    if data['password'] != "":
        user.password = make_password(data['password'])
        
    user.save()
    profile.save()
    serializer = ProviderSerializer(profile)    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    user = request.user
    provider = get_object_or_404(Providerprofile,id=pk)
    data = request.data
    review = provider.reviews.filter(user=user)
   
    if data['rating'] <= 0 or data['rating'] > 10:
        return Response({"error":'Please select between 1 to 5 only'}
                        ,status=status.HTTP_400_BAD_REQUEST) 
    elif review.exists():
        new_review = {'rating':data['rating'], 'comment':data['comment'] }
        review.update(**new_review)

        rating = provider.reviews.aggregate(avg_ratings = Avg('rating'))
        provider.ratings = rating['avg_ratings']
        provider.save()

        return Response({'details':'Product review updated'})
    else:
        Review.objects.create(
            user=user,
            provider=provider,
            rating= data['rating'],
        )
        rating = provider.reviews.aggregate(avg_ratings = Avg('rating'))
        provider.ratings = rating['avg_ratings']
        provider.save()
        return Response({'details':'Product review created'})


@api_view(['GET']) 
def allprovider(request,pk):
    filterset = ProvidersFilter(request.GET,queryset=Providerprofile.objects.filter(service_id=pk).order_by('id'))
    serializer = GetprovidersSerializer(filterset.qs,many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def provider_favourite(request,pro_id):
        pro_fav=Providerprofile.objects.get(pk=pro_id)
        if Userprofile.objects.filter(user=request.user,provider_favourites=pro_fav).exists()==False:
            userprofile=Userprofile.objects.get(user=request.user)
            userprofile.provider_favourites.add(pro_fav)
            return Response('product add to favourites')
        else:
            return Response(request,'Already product in favorite list')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_favourites(request):
    userInfo = Userprofile.objects.get(user=request.user)
    serializer = GetallFavourites(userInfo)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if len(new_password) < 8:
        return Response({'message':'The min length of password is 8 numbers'},status=status.HTTP_400_BAD_REQUEST)
    
    if not check_password(old_password,user.password):
        return Response({'message':'The old password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
      
    user.save()
    update_session_auth_hash(request,user)
    return Response({'message':'the password is updated'})