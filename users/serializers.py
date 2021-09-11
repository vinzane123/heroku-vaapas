from users.models import *
from rest_framework import exceptions
from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self,data):
        phone = data.get("phone","")
        
        if phone:
            user=User.objects.filter(phone=phone)
            if user:
                    data["user"] = user[0]
            else:
                msg = "Incorrect Credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Please provide your phone number."
            raise exceptions.ValidationError(msg)
        return data
    
class OTPSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields=['phone','otp']

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['phone','timestamp']

class UserDataSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserData
            fields = ['phone','smsData','callLogs','contactList','permissionGiven','interested','Responses']
              