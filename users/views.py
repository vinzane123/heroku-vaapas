from .models import User,UserData
from .serializers import *
from users import factor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import mixins,filters,generics

from django.shortcuts import render,get_object_or_404,HttpResponse
from django.contrib.auth import login as django_login, logout as django_logout

from drf_yasg.utils import swagger_auto_schema

# Create your views here.

import json,time,random,datetime,requests,logging

'''
Index Page., Home URL
'''
def index(request):
    return HttpResponse('Hail, Login Service!')


class LoginWithOtp(APIView):

    @swagger_auto_schema(request_body=LoginSerializer,operation_description="Login mobile number")
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            if time.time() - user.timeCounter>123:
                send_otp(user)
                return Response({
                    'status':True,
                    'statusCode':204,
                    'details':'OTP sent. Please validate the same.'
                })
            else:
                return Response({'details':'OTP is not expired yet.'},status=405) 
        else:
            user = User.objects.create(phone=request.data['phone'])
            user.save()
            userData = UserData.objects.create(phone=user,permissionGiven=True)
            userData.save()
            send_otp(user)
            return Response({
                'status':True,
                'statusCode':204,
                'details':'OTP sent. Please validate the same.'
            })              

def send_otp(user):
    otp = User.objects.get(phone=user.phone)
    key = random.randint(99999,1000000)
    otp.otp=key
    otp.timeCounter=time.time()
    otp.validated = False
    otp.save()
    factor.payload['To'] = user.phone
    factor.payload['VAR1'] = key    
    factor.payload['VAR2'] ='N6coML6fsFl'
    payload = factor.payload
    print(key)
    requests.request("POST", factor.url, data = factor.payload, files = factor.files)


class LogoutView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer,operation_description="Logout of the session")
    def post(self,request):
        user = User.objects.get(phone=request.data['phone'])
        user.validated=False
        user.save()
        django_logout()
        return Response(status=204)
        

class ValidateWithOtp(APIView):

    @swagger_auto_schema(request_body=OTPSerializer,operation_description="Verify with OTP")
    def post(self,request):
        try:
            phone=request.data['phone']
            otp = User.objects.get(phone=phone,otp=request.data['otp'])
            if time.time()-otp.timeCounter>123:
                return Response(
                    status=200,
                    data={'details':'OTP Expired. Please login again.'}
                )
            else:
                otp.validated = True
                otp.save()
                serializer = LoginSerializer(data=request.data)
                if serializer.is_valid():
                    user = serializer.validated_data["user"]
                    return Response({
                        'status':True,
                        'details':'Validation Successful. You are Logged in.',
                        'user':user.phone,
                    })      
        except:
            return Response({
                    'status':False,
                    'details':'Incorrect Credentials provided'
                },status=403)                          

class UserIO(mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        generics.GenericAPIView):
    
    serializer_class = UserDataSerializer
    queryset = UserData.objects.all()
    lookup_field='phone'

    @swagger_auto_schema(responses={200: UserDataSerializer(many=True)},operation_description="Get all users data.")
    def list(self, request):
        queryset = UserData.objects.all()
        serializer = UserDataSerializer(queryset,many=True)
        return Response(serializer.data,status=200)        

    @swagger_auto_schema(responses={200: LoginSerializer(many=True)},operation_description="Get User related data.")
    def get(self,request,phone=None):
        if phone:
            try:
                user = User.objects.get(phone=phone)
                queryset = UserData.objects.filter(phone=user)
                serializer = UserDataSerializer(queryset,many=True)
                return Response(serializer.data,status=200)
            except:
                return Response({
                'status':401,
                'details':'Something went wrong. User not found'
            })

        else:
            return self.list(request)            
        
    @swagger_auto_schema(request_body=UserDataSerializer,operation_description="Add UserData")
    def post(self,request,phone):
        try:
            user = User.objects.get(phone=phone)
            user.validated
            userdata = UserData.objects.get(phone=user)
            user.permissionGiven = request.data['permissionGiven']
            userdata.smsData = request.data['smsData']
            userdata.callLogs = request.data['callLogs']
            userdata.contactList = request.data['contactList']
            userdata.save()
            return Response({
                'status':200
            })
        except:
            return Response({
                'status':401,
                'details':'Something went wrong. User not found'
            })
    
    @swagger_auto_schema(request_body=UserDataSerializer,operation_description="Update UserData")
    def put(self,request,phone):
        try:
            user = User.objects.get(phone=phone)
            user.validated
            userdata = UserData.objects.get(phone=user)
            userdata.interested = request.data['interested']
            userdata.Responses = request.data['Responses']
            userdata.save()
            return Response({
                    'status':200,
                    'details':'Updated successfully'
                })
        except:
            return Response({
                'status':404,
                'details':'User not found.'
            })