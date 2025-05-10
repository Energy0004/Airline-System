from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from unicodedata import normalize
from .models import Flight, Booking, Passenger, Airport
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
        read_only_fields = ['id', 'is_staff']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    second_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'second_password', 'tokens']

    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)

        refresh['username'] = obj.username
        refresh['email'] = obj.email
        refresh['isAdmin'] = obj.is_staff

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['second_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username__iexact=obj['username'])
        refresh = RefreshToken.for_user(user)

        refresh['username'] = user.username
        refresh['email'] = user.email
        refresh['isAdmin'] = user.is_staff

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            normalized_username = username.lower()
            try:
                user_obj = User.objects.get(username__iexact=normalized_username)
                logger.debug(f"Found user: {user_obj.username}")
            except User.DoesNotExist:
                logger.warning(f"Login failed: username '{normalized_username}' not found")
                raise serializers.ValidationError(
                    'Invalid username or password.',
                    code='authorization'
                )
            user = authenticate(
                request=self.context.get('request'),
                username=user_obj.username,
                password=password
            )
            if not user:
                logger.warning(f"Authentication failed for username: {normalized_username}")
                raise serializers.ValidationError(
                    'Invalid username or password.',
                    code='authorization'
                )
            if not user.is_active:
                logger.warning(f"Inactive user tried to login: {normalized_username}")
                raise serializers.ValidationError(
                    'This account is inactive.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "username" and "password".',
                code='authorization'
            )
        attrs['user'] = user
        return attrs

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def update(self, instance, validated_data):
        if 'password' in validated_data and validated_data['password']:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'city_name', 'code']

class FlightSerializer(serializers.ModelSerializer):
    passengers = serializers.SerializerMethodField()
    origin = AirportSerializer()
    destination = AirportSerializer()
    class Meta:
        model = Flight
        fields = ['id', 'origin', 'destination', 'duration', 'capacity', 'passengers']

    def get_passengers(self, obj):
        bookings = Booking.objects.filter(flight=obj)
        return PassengerSerializer([b.passenger for b in bookings], many=True).data

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['name', 'email']

class BookingCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_code']

class BookingSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer()
    flight = FlightSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'passenger', 'flight', 'created_at', 'booking_code', 'user']