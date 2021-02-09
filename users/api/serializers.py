from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
# from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
# Serializers define the API representation.
from users.models import UserProfile
User = get_user_model()


# class CustomRegisterSerializer(RegisterSerializer):
#     """
#     Custom User Registeration Serializer Inhereting from rest_auth RegisterSerializer
#     """
#     # email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
#     email = None


class CustomLoginSerializer(LoginSerializer):
    """
    Custom User Login Serializer Inhereting from rest_auth LoginSerializer

    """
    # renderer_classes = [JSONRenderer]
    # email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)

    # def validate(self, attrs):
    #     attrs = super(CustomLoginSerializer, self).validate(attrs)
    #     print(attrs)
    #     return attrs
    # print(self.data())

    # def data(self, *args, **kwargs):
    #     data = super().data(*args, **kwargs)
    #     print(data)
    #     return data
    def get_serializer_context(self, *args, **kwargs):
        context = super(CustomLoginSerializer).get_serializer_context(
            *args, **kwargs)

        print(context)
        context['message'] = 'No Message'
        # context.update({"request": self.request})
        return context

    email = None


class ListAllUserSerializer(serializers.ModelSerializer):
    '''
    Show all users list
    '''
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'date_joined']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Show user attached with a url"""

    class Meta:
        model = get_user_model()
        # fields = ['url', 'username', 'email','date_joined',]
        fields = ['url', 'username', ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """ Show Group attached with a url"""
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'last_login', ]


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['url', 'user', 'image',]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'last_login',
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
