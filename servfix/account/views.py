from django.db.models import Avg
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status , viewsets
from .serializers import SignUpSerializer,UserSerializer,ProviderSignUpSerializer,ProviderSerializer,RoleSerializer2,GetprovidersSerializer ,AddTowork,SelectedProvider,RoleSerializer,ImageSerializer , Getallfavourite
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from account.models import Userprofile,Providerprofile , Review,Work, IMage , UserProviderFavourite
from service.models import Service  
from .filtters import ProvidersFilter
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
import re
from django.contrib.auth import authenticate ,logout
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import SessionAuthentication

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data = data)
    if user.is_valid():
        if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists():
            regex = r'\b[A-Za-z0-9._%+-]+@gmail+\.[A-Z|a-z]{2,7}\b'
            pattern = re.compile(r"^[0-9]+$")
            match = re.search(pattern, data['phone'])
            if(match):
                if(re.fullmatch(regex, data['email'])):
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
                {'eroor':'enter a real gamil' },
                    status=status.HTTP_400_BAD_REQUEST
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_role(request):
    profile1 = Userprofile.objects.filter(user=request.user)
    profile2 = Providerprofile.objects.filter(user=request.user)
    serializer = RoleSerializer(profile1,many=True)
    serializer2= RoleSerializer2(profile2,many=True)
    if(serializer.data):
       return Response(serializer.data)
    else:
     return Response(serializer2.data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    profile = Userprofile.objects.get(user=request.user)
    user = request.user
    data = request.data
    username=user.username
    email=user.email
    regex = r'\b[A-Za-z0-9._%+-]+@gmail+\.[A-Z|a-z]{2,7}\b'
    pattern = re.compile(r"^[0-9]+$")
    match = re.search(pattern, data['phone'])
    if(match):
        if(re.fullmatch(regex, data['email'])):
            if(user.username!=data['username']):
                if not User.objects.filter(username=data['username']).exists():
                    username=data['username']
                else:  
                    return Response(
                    {'eroor':'This  username already exists!' },
                        status=status.HTTP_400_BAD_REQUEST
                        )   

            if(user.email!=data['email']):
                if not User.objects.filter(email=data['email']).exists():
                  email=data['email']  
                else:  
                    return Response(
                    {'eroor':'This  email already exists!' },
                        status=status.HTTP_400_BAD_REQUEST
                        )  
                
            user.username = username
            profile.username = username
            user.email = email
            profile.email = email
            phone_prefix = data['phone'][:3]
            valid_prefixes = ['010','012','011','015']
            if len(data['phone'])!=11:
                return Response ({'error':'the phone should be 11 number'},status=status.HTTP_400_BAD_REQUEST)
            
            elif phone_prefix not in valid_prefixes:
                return Response({'error':'phone number should startwith 010 or 011 or 012 or 015'},status=status.HTTP_400_BAD_REQUEST)
            
            else: 
                profile.phone = data['phone']
                profile.address = data['address']
                profile.city = data['city']
                profile.image = data['image']  
                user.save()
                profile.save()
                serializer = UserSerializer(profile)
            return Response(serializer.data) 
        else:
            return Response(
        {'eroor':'enter a valid gmail' },
            status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(
        {'eroor':'only numbers accepted' },
            status=status.HTTP_400_BAD_REQUEST
            )
 


  
def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)



@api_view(['POST'])
def forgot_password2(request):
    data = request.data
    if 'email' not in data:
        return Response({'error':'Email is required'},status=status.HTTP_400_BAD_REQUEST)
    # user = get_object_or_404(User , email=data['email'])
    token=data['email']
    return Response({'id':'{token}'.format(token=token)},status=status.HTTP_200_OK)



@api_view(['POST'])
def forgot_password(request):
    data = request.data
    if 'email' not in data:
        return Response({'error':'Email is required'},status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User , email=data['email'])

    # Generate the password reset token and link
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    host = get_current_host(request)
    link = "https://p2kjdbr8-8000.uks1.devtunnels.ms/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)

    # Send the password reset email to the user's email address
    send_mail(
        "Password reset from servfix",
        body,
        "servfix2023@gmail.com",  # Use your Gmail account here
        [user.email]  # Use the user's email from the database
    )

    return Response({'details': 'Password reset sent to {email}'.format(email=user.email)})



@api_view(['POST'])
def reset_password2(request,token):
    data = request.data
    user = get_object_or_404(User,email = token)


    
    if len(data['password']) < 8:
        return Response({'error':'The min length of password is 8 numbers'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    if check_password(data['password'],user.password):
        return Response({'error':'This is old password please enter new one'},status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None 
    user.profile.save() 
    user.save()
    return Response({'details': 'Password reset done '})



@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(User,profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    
    if len(data['password']) < 8:
        return Response({'error':'The min length of password is 8 numbers'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    if check_password(data['password'],user.password):
        return Response({'error':'This is old password please enter new one'},status=status.HTTP_400_BAD_REQUEST)
    
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
          serv= Service.objects.get(name=data['profession'])
          if not User.objects.filter(email=data['email']).exists() and not User.objects.filter(username=data['username']).exists() :
             regex = r'\b[A-Za-z0-9._%+-]+@gmail+\.[A-Z|a-z]{2,7}\b'
             pattern = re.compile(r"^[0-9]+$")
             match = re.search(pattern, data['phone'])
             match2 = re.search(pattern, data['fixed_salary'])
             if(match and match2):
                if(re.fullmatch(regex, data['email'])):
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
                {'eroor':'enter a valid gmail' },
                    status=status.HTTP_400_BAD_REQUEST
                    )
             else:
                 return Response(
                {'eroor':'only numbers accepted in phone and salary' },
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
    regex = r'\b[A-Za-z0-9._%+-]+@gmail+\.[A-Z|a-z]{2,7}\b'
    username=user.username
    email=user.email
    pattern = re.compile(r"^[0-9]+$")
    match = re.search(pattern, data['phone'])
    match2 = re.search(pattern, data['fixed_salary'])

    if(match and match2):
        if(re.fullmatch(regex, data['email'])):
            if(user.username!=data['username']):
                if not User.objects.filter(username=data['username']).exists():
                    username=data['username']
                else:  
                    return Response(
                    {'eroor':'This  username already exists!' },
                        status=status.HTTP_400_BAD_REQUEST
                        )   

            if(user.email!=data['email']):
                if not User.objects.filter(email=data['email']).exists():
                  email=data['email']  
                else:  
                    return Response(
                    {'eroor':'This  email already exists!' },
                        status=status.HTTP_400_BAD_REQUEST
                        )
            user.username = data['username']
            profile.username = data['username']
            user.email = data['email']
            profile.email = data['email']
            phone_prefix = data['phone'][:3]
            valid_prefixes = ['010','012','011','015']
            if len(data['phone'])!=11:
                return Response ({'error':'the phone should be 11 number'},status=status.HTTP_400_BAD_REQUEST)
            
            elif phone_prefix not in valid_prefixes:
                return Response({'error':'phone number should startwith 010 or 011 or 012 or 015'},status=status.HTTP_400_BAD_REQUEST)
            
            else: 
                profile.phone = data['phone']
                profile.address = data['address']
                profile.city = data['city']
                # profile.profession = data['profession']
                profile.fixed_salary = data['fixed_salary']
                profile.image = data['image']
                user.save()
                profile.save()
                serializer = ProviderSerializer(profile)    
                return Response(serializer.data)
        else:
            return Response(
        {'eroor':'enter a valid gmail' },
            status=status.HTTP_400_BAD_REQUEST
            )

    else:
        return Response(
        {'eroor':'only numbers accepted in salary and phone' },
            status=status.HTTP_400_BAD_REQUEST
            )

        



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
        new_review = {'rating':data['rating']}
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
    count = filterset.qs.count()
    resPage = 12
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    queryset =  paginator.paginate_queryset(filterset.qs, request)
    serializer = GetprovidersSerializer(queryset,many=True)
    return Response({"providers":serializer.data, "per page":resPage, "count":count})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def provider_favourite(request,prov_id):
    prov_fav=Providerprofile.objects.get(pk=prov_id)
    userprofile=Userprofile.objects.get(user=request.user)
    if UserProviderFavourite.objects.filter(user=userprofile,provider_favourite=prov_fav).exists()==False:
        UserProviderFavourite.objects.create(user=userprofile,provider_favourite=prov_fav,is_favourite=True)
        return Response({'details':'provider add to favourites'})
    
    elif UserProviderFavourite.objects.filter(user=userprofile,provider_favourite=prov_fav,is_favourite=True).exists()==False:
        UserProviderFavourite.objects.filter(user=userprofile,provider_favourite=prov_fav).update(is_favourite=True)
        return Response({'details':'provider add to favourites'})
    
    else:
        return Response({'details':'Already provider in favourite list'},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_favourites(request):
    userInfo = Userprofile.objects.get(user=request.user)
    favourites = UserProviderFavourite.objects.filter(user=userInfo, is_favourite=True)
    serializer = Getallfavourite(favourites, many=True)
    return Response({'provider_favourite':serializer.data})


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_work(request):
    serializer = AddTowork(data=request.data)
    if serializer.is_valid():
        provider_profile = Providerprofile.objects.get(user=request.user)
        serializer.save(provider_id=provider_profile)
        return Response({'message':'The work added successfully'},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def selected_provider(request,sele_id):
    sele_prov=Providerprofile.objects.get(pk=sele_id)
    user = Userprofile.objects.get(user=request.user)
    provider_works = IMage.objects.all().filter(work__provider_id=sele_prov)
    user_provider_favourite = UserProviderFavourite.objects.filter(user=user,provider_favourite=sele_prov).first()
    is_favourite = user_provider_favourite.is_favourite if user_provider_favourite else False
    provider_serializer = SelectedProvider(sele_prov)
    work_serializer = ImageSerializer(provider_works,many=True)
    response_data = {
        'provider':provider_serializer.data,
        'works':work_serializer.data,
        'is_favourite': is_favourite
    }
    return Response(response_data)





@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def All_jobs(request):
    provider_id = Providerprofile.objects.get(user=request.user)
    images = IMage.objects.all().filter(work__provider_id=provider_id)
    serializer = ImageSerializer(images,many=True)
    return Response(serializer.data)




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_work(request,image_id):
    image = get_object_or_404(IMage,id=image_id)
    image.delete()
    return Response({'details':'The image deleted successfully'},status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favourite(request,fav_id):   
    userprofile = Userprofile.objects.get(user=request.user)
    fav_delete = Providerprofile.objects.get(id=fav_id)
    UserProviderFavourite.objects.filter(user=userprofile,provider_favourite=fav_delete).update(is_favourite=False)
    return Response({'details':'the fav deleted successfully'},status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_providers_for_service(request,pk):
    filterset = ProvidersFilter(request.GET,queryset=Providerprofile.objects.filter(service_id=pk).order_by('id'))
    count = filterset.qs.count()
    resPage = 12
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    queryset =  paginator.paginate_queryset(filterset.qs, request)
    serializer = GetprovidersSerializer(queryset,many=True)
    return Response({"providers":serializer.data, "per page":resPage, "count":count})



class DeleteAccountView(APIView): 
    def delete(self, request): 
 
        # serializer = PasswordSerializer(data=request.data) 
         
        # if serializer.is_valid(): 
            # password = serializer.validated_data.get('password') 
        user = request.user 

        if not user.is_authenticated: 
            return Response({"error": "Authentication credentials were not provided"}, status=status.HTTP_401_UNAUTHORIZED) 

        # if not user.check_password(password): 
        #     return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST) 

        user.delete() 
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK) 
        # else: 
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
         
         
class LogoutAPIView(APIView): 
    permission_classes = [IsAuthenticated]
    def post(self, request): 
        logout(request)  # Clear user's session  
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)