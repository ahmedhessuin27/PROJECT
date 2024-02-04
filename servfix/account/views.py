from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SingUpSerializer, UserSerializer
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from account.models import Userprofile
from .emails import *


class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = Userprofile.objects.get(user=request.user)
        user_info = {
            "email": user_profile.user.email,
            "username": user_profile.user.username,
            "phone": user_profile.phone,
            "city": user_profile.city,
            "address": user_profile.address,
        }

        return Response(data=user_info, status=status.HTTP_200_OK)


class ResendOtpAPI(APIView):
    def post(self, request):
        try:
            serializer = ResendOtpSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                user = Userprofile.objects.filter(user__email=email).first()
                if user:
                    if not user.is_verified:
                        send_otp_via_email(email)
                        return Response(
                            data={
                                "status": status.HTTP_200_OK,
                                "message": "OTP sent successfully",
                                "data": {},
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {
                                "status": 400,
                                "message": "User already verified, please login",
                                "data": {},
                            }
                        )
                else:
                    return Response(
                        {
                            "status": 404,
                            "message": "User not found",
                            "data": {},
                        }
                    )
            else:
                return Response(
                    {
                        "status": 400,
                        "message": "Incorrect email",
                        "data": {},
                    }
                )
        except Exception as e:
            print(e)

            return Response({"error": str(e), "status": 500})


class RegisterAPI(APIView):
    def post(self, request):
        try:
            serializer = SingUpSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                if not User.objects.filter(
                    email=data["email"]
                ).exists():
                    user = User.objects.create(
                        email=data["email"],
                        password=make_password(data["password"]),
                        username=data["username"],
                    )
                    Userprofile.objects.create(
                        user=user,
                        address=data["address"],
                        phone=data["phone"],
                        city=data["city"],
                    )
                    send_otp_via_email(data["email"])
                    return Response(
                        data={
                            "status": status.HTTP_200_OK,
                            "message": "Registration Successfully Check email",
                            "data": serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
            return Response(
                {
                    "status": 400,
                    "message": "Something went wrong",
                    "data": serializer.errors,
                }
            )
        except Exception as e:
            print(e)

            return Response({"error": str(e)})


class VerifyOTP(APIView):
    def post(self, request):
        try:
            
            serializer = VerifyAccountSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data
                email = data["email"]
                otp = data["otp"]
                user = Userprofile.objects.filter(user__email=email).first()
                if user is None:
                    return Response(
                        {
                            "status": 400,
                            "message": "Something went wrong",
                            "data": "Invalid email",
                        }
                    )
                if user.otp != otp:
                    return Response(
                        {
                            "status": 400,
                            "message": "Something went wrong",
                            "data": "Wrong otp",
                        }
                    )
                user.is_verified = True
                user.save()

                return Response(
                    {
                        "status": 200,
                        "message": "Account Verified",
                        "data": {},
                    }
                )
            return Response(
                {
                    "status": 400,
                    "message": "Something went wrong",
                    "data": serializer.errors,
                }
            )
        except Exception as e:
            print(e)
