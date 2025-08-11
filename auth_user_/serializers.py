from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50)
    confirm_password = serializers.CharField(max_length=50,write_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name",'last_name','username','age','address','password','confirm_password']

    def validate(self, data):
        if data["password"] != data['confirm_password']:
            raise ValidationError({'message':"parollar mos emas",'status':status.HTTP_400_BAD_REQUEST})
        username = data['username']
        if  CustomUser.objects.filter(username = username).exists():
            raise ValidationError({'message':"Bu username oldin ruyxatdan utgan",'status':status.HTTP_400_BAD_REQUEST})
        return data

    def create(self,validated_data):
        validated_data.pop("confirm_password")
        user = CustomUser(
            username = validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            age=validated_data["age"],
            address=validated_data["address"],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        user.token = token.key
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        if not data['username'] or not data['password']:
            raise ValidationError({"error":"Login yoki parol kiritilmadi","status":status.HTTP_400_BAD_REQUEST})
        try:
            user = authenticate(username = data['username'], password = data['password'])
            if user is None:
                raise ValidationError({
                    "error": "Login yoki parol noto'g'ri",
                    "status": status.HTTP_400_BAD_REQUEST
                })
            token , _ = Token.objects.get_or_create(user = user)
        except Exception as e:
            raise ValidationError({"error": "Login yoki parol noto'g'ri",'status':status.HTTP_400_BAD_REQUEST})
        data['token'] = token.key
        return data


class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"