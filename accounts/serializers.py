from cgitb import lookup
from unittest.util import _MAX_LENGTH
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from django.contrib.auth import authenticate,login

# from .models import Nps_Survey
from .utils import get_tokens_for_user
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from employer_profile.models import EmployerDetails
import time
from resume.serializers import CreatableSlugRelatedField
CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """
    We use this serializer for user registration. Most of the fields have
    `required=False`, but can be configured as needed. This serializer is used
    in `accounts.viewsets.CustomUserModelViewSet`.
    """

    email = serializers.CharField(
        validators=[validators.UniqueValidator(
            message='This email already exists',
            queryset=CustomUser.objects.all()
        )]
    )
    password = serializers.CharField(write_only=True)
    # bio = serializers.CharField(required=False)
    # gender = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    # birth_date = serializers.CharField(required=False)
    id=serializers.UUIDField(required=False)

    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'email',
                  'password', 'type')

    
    def validate(self, args):
        email = args.get('email', None)
        
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('email already exists')})
        
        return super().validate(args)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
# class EmployerDetailsSerializer(serializers.ModelSerializer):
#     user=serializers.CharField()
#     company_name=serializers.CharField(max_length=100)

#     class Meta:
#         model = EmployerDetails
#         fields = '__all__'
#         # lookup_field='user_email'
    
# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployerDetails
#         fields = '__all__'  # ('job_title','user_id')
#         lookup_field = "user_id"

class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    """
    We use this serializer to retrieve data of the currently logged in user.
    It is used in `accounts.views.UserRetrieveUpdateDestroyAPIView`
    """
    birth_date = serializers.CharField(required=False,allow_null=True)
    bio = serializers.CharField(required=False,allow_null=True)
    gender = serializers.CharField(required=False,allow_null=True)
    nps=serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_login=serializers.DateTimeField(read_only=True,allow_null=True)
    Lastlogin1=serializers.DateTimeField(read_only=True,allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                  'bio', 'gender', 'birth_date','id','type','is_verified','nps','pmf','last_login','feedback','Lastlogin1')

    def validate_nps(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

class CustomUserTestSerializer(serializers.ModelSerializer):
    # nps = serializers.IntegerField(initial=0, allow_null=True)
    nps=serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_login=serializers.DateTimeField(read_only=True,allow_null=True)
    Lastlogin1=serializers.DateTimeField(read_only=True,allow_null=True)
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',
                   'id','nps','pmf','last_login','feedback','Lastlogin1')
    def validate_nps(self, value):
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            raise serializers.ValidationError('You must supply an integer')

# class AllUserDataSerializer(serializers.ModelSerializer):
#     # user=CustomUserSerializer(required=False,many=True)
#     user=CustomUserTestSerializer(read_only=True)
#     # user= CreatableSlugRelatedField(
#     #     queryset=CustomUser.objects.all(),
#     #     many=True,
#     #     slug_field='id',
#     #     allow_null=True,
#     #     # required=False
#     #  )


#     class Meta:
#         model=Nps_Survey
#         fields = ['id','user','Nps','Pmf','Last_login','Feedback']
#         depth= 1

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = CustomUser.objects.create(**user_data)
    #     nps = Nps_Survey.objects.create(user=user, **validated_data)
    #     return nps      
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    first_name= serializers.CharField(read_only=True)
    last_name= serializers.CharField(read_only=True)
    id=serializers.UUIDField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        # startT = time.time()
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = get_tokens_for_user(user)
            refresh_token = str(refresh['refresh'])
            access_token = str(refresh['access'])


            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'type': user.type,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'id':user.id,
            }
            # print(f' 1st function time: {time.time() - startT}ms')
            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()

    class Meta:
        model=CustomUser
        fields = ['email']

class ResetPasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    class Meta:
        model=CustomUser
        fields = ['password1','password2']


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

