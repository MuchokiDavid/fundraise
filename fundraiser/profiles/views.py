from django.shortcuts import render
from django.db.models import Q
import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config
import datetime as dt
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from oauth2_provider.models import Application, AccessToken, RefreshToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from .utility import generate_random_otp, create_token

OAUTH_CLIENT_ID = config('OAUTH_CLIENT_ID')
OAUTH_SECRET_ID = config('OAUTH_SECRET_ID')
logger = logging.getLogger(__name__)

# Create your views here.
class SignUp(APIView):
    def post(self, request):
        try:
            data = request.data
            email= data.get('email')
            phone = data.get('phone_number')
            national_id = data.get('national_id')
            
            if User.objects.filter(Q(email=email) | Q(phone_number=phone) | Q(national_id=national_id)).exists():
                return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error signing up user: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class LogIn(APIView):
    def post(self, request):
        try:
          username = request.data.get('email')
          password = request.data.get('password')

          if not username or not password:
              return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

          user = User.objects.filter(email=username).first()

          if not user:
              return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

          if user.is_active == False:
                  return Response({'error': 'User is not active'}, status=status.HTTP_406_NOT_ACCEPTABLE)
              
          user = authenticate(email=username, password=password)
          if not user:
              return Response({'error': 'Invalid password'}, status=status.HTTP_403_FORBIDDEN)
          
          try:
              application = Application.objects.get(client_id= OAUTH_CLIENT_ID)
          except Application.DoesNotExist:
              return Response({'error': 'Invalid client credentials'}, status=status.HTTP_403_FORBIDDEN)
          
          # Revoke any existing tokens
          AccessToken.objects.filter(user=user, application=application).delete()
          RefreshToken.objects.filter(user=user, application=application).delete()
          
          expires = dt.datetime.now() + timedelta(days=1)
          scope = 'read write'
          # Create new access token
          access_token = AccessToken.objects.create(
              user=user,
              application=application,
              token=create_token(),
              expires=expires,
              scope=scope
          )
          
          # Create refresh token
          refresh_token = RefreshToken.objects.create(
              user=user,
              application=application,
              token=create_token(),
              access_token=access_token
          )

          login(request, user)
          return Response({
              'access_token': access_token.token,
              'expires_in': 3600*24,
              'token_type': 'Bearer',
              'scope': access_token.scope,
              'refresh_token': refresh_token.token,
              'user': UserSerializer(user).data
          })
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogOut(APIView):
    authentication_classes= [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,  IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            tokens=  AccessToken.objects.filter(user=request.user)
            for token in tokens:
                token.delete()
            
            refresh_tokens=  RefreshToken.objects.filter(user=request.user)
            for token in refresh_tokens:
                token.delete()
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error logging out user: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RefreshTokenView(APIView):
    def post(self, request):
        try:
          refresh_token = request.data.get('refresh_token')
          if not refresh_token:
              return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

          try:
              refresh_token = RefreshToken.objects.get(token=refresh_token)
          except RefreshToken.DoesNotExist:
              return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

          # Revoke the old access token
          AccessToken.objects.filter(user=refresh_token.user, application=refresh_token.application).delete()

          # Create new access token
          new_access_token = AccessToken.objects.create(
              user=refresh_token.user,
              application=refresh_token.application,
              token=create_token(),
              expires=dt.datetime.now() + timedelta(days=1),
              scope='read write'
          )

          # Update the refresh token
          refresh_token.access_token = new_access_token
          refresh_token.save()

          return Response({
              'access_token': new_access_token.token,
              'expires_in': 3600*24,
              'token_type': 'Bearer',
              'scope': new_access_token.scope,
              'refresh_token': refresh_token.token,
              'user': UserSerializer(refresh_token.user).data
          })
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserView(APIView):
    authentication_classes= [OAuth2Authentication]
    permission_classes = [TokenHasReadWriteScope,  IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
class ResetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp = generate_random_otp()
            user.otp = otp
            user.otp_expiry = dt.datetime.now() + dt.timedelta(minutes=10)
            user.save()
            # Send OTP to user's email
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"User with email {email} not found")
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ChangePassword(APIView):
    def post(self, request):
        try:
            data = request.data
            # username = data.get('username')
            otp= data.get('otp')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            user = User.objects.filter(otp=otp).first()
            if user is None:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            if not otp:
                return Response({'error': 'OTP is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not password or not confirm_password:
                return Response({'error': 'Password and confirm password are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.otp_expiry < timezone.now():
                user.otp = None
                user.otp_expiry = None
                user.save()
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.otp != otp:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            
            if password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.otp = None
            user.otp_expiry = None
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error in ChangePassword.post: {e}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
