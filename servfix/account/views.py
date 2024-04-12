from django.db.models import Avg
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status , viewsets
from .serializers import SignUpSerializer,UserSerializer,ProviderSignUpSerializer,ProviderSerializer,GetprovidersSerializer , GetallFavourites,AddTowork,SelectedProvider,AllWork
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from account.models import Userprofile,Providerprofile , Review,Work
from service.models import Service  
from .filtters import ProvidersFilter
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from rest_framework.views import APIView
import os
import re

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data = data)
    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists():
            pattern = re.compile(r"^[0-9]+$")
            match = re.search(pattern, data['phone'])
            if(match):
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
                {'eroor':'only numbers accepted' },
                    status=status.HTTP_400_BAD_REQUEST
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
    # if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists():
    #         pattern = re.compile(r"^[0-9]+$")
    #         match = re.search(pattern, data['phone'])
    #         if(match):
    
    user.username = data['username']
    profile.username = data['username']
    user.email = data['email']
    profile.email = data['email']
    profile.phone = data['phone']
    profile.address = data['address']
    profile.city = data['city']
    profile.image = data['image']  
        
    user.save()
    profile.save()
    serializer = UserSerializer(profile)
    return Response(serializer.data) 
            # else:
            #     return Response(
            #     {'eroor':'only numbers accepted' },
            #         status=status.HTTP_400_BAD_REQUEST
            #         )

    # else:     
    #         return Response(
    #             {'eroor':'This email or username already exists!' },
    #                 status=status.HTTP_400_BAD_REQUEST
    #                 )   


  
def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)



@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])

    # Generate the password reset token and link
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = "http://127.0.0.1:8000/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)

    # Send the password reset email to the user's email address
    send_mail(
        "Password reset from servfix",
        body,
        "your-gmail-account@gmail.com",  # Use your Gmail account here
        [user.email]  # Use the user's email from the database
    )

    return Response({'details': 'Password reset sent to {email}'.format(email=user.email)})


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
            # id_image = serializer.validated_data.get('id_image')
            # try:
            #     img = Image.open(id_image)
            #     if img.size != (213,153):
            #         return Response({'error':'This image not ID image'},status=status.HTTP_400_BAD_REQUEST)
            # except Exception as e:
            # 
            #         return Response({'error':'Habben error during scan the image'},status=status.HTTP_400_BAD_REQUEST)
        #  else:
            # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
          serv= Service.objects.get(name=data['profession'])
          
          if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists() :
             
             pattern = re.compile(r"^[0-9]+$")
             match = re.search(pattern, data['phone'])
             match2 = re.search(pattern, data['fixed_salary'])

             if(match or match2):
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
                {'eroor':'only numbers accepted' },
                    status=status.HTTP_400_BAD_REQUEST
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

        return Response({'details':'provider review updated'})
    else:
        Review.objects.create(
            user=user,
            provider=provider,
            rating= data['rating'],
        )
        rating = provider.reviews.aggregate(avg_ratings = Avg('rating'))
        provider.ratings = rating['avg_ratings']
        provider.save()
        return Response({'details':'provider review created'})


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
            return Response('provider add to favourites')
        else:
            return Response(request,'Already provider in favorite list')


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


class ADDwork(ModelViewSet):
    # queryset=Work.objects.all()
    # serializer = AddTowork
    # parser_classes=(MultiPartParser,FormParser)
    # def create(self, request, *args, **kwargs):
    #     image=request.data["image"]
    #     Work.objects.create(image=image)
    #     return Response({'message':'The work added successfully'},status=status.HTTP_201_CREATED)
    # @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        serializer = AddTowork(data=request.data)
        if serializer.is_valid():
            provider_profile = Providerprofile.objects.get(user=request.user)
            image=request.data["image"]
            Work.objects.create(image=image , provider_id=provider_profile)
            # serializer.save(provider_id=provider_profile)
            return Response({'message':'The work added successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def selected_provider(request,sele_id):
    sele_prov=Providerprofile.objects.get(pk=sele_id)
    provider_works = Work.objects.filter(provider_id=sele_prov)
    provider_serializer = SelectedProvider(sele_prov)
    work_serializer = AllWork(provider_works,many=True)
    response_data = {
        'provider':provider_serializer.data,
        'works':work_serializer.data
    }
    return Response(response_data)





# class W(viewsets.ModelViewSet ):
class getimage(APIView):
    # @api_view(['GET']) 
    # @permission_classes([IsAuthenticated])
    def get(self,request,*args,**kwargs):
        provider_id = Providerprofile.objects.get(user=request.user)
        image = Work.objects.all().filter(provider_id=provider_id)
        serializer = AllWork(image , many =True)
        return Response(serializer.data , status= status.HTTP_200_OK)



# class getimage(APIView):
#     def get(self,request,*args,**kwargs):
#         image=imageodel.objects.all()
#         serializer=ImageSerializer(image,context = {'request': request} , many =True)
#         return Response(serializer.data , status= status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_work(request,work_id):
    image = get_object_or_404(Work,id=work_id)
    image.delete()
    return Response({'details':'The work deleted successfully'})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favourite(request,fav_id):
    userprofile = Userprofile.objects.get(user=request.user)
    fav_delete = Providerprofile.objects.get(id=fav_id)
    userprofile.provider_favourites.remove(fav_delete)
    return Response({'details':'the fav deleted successfuly'})


