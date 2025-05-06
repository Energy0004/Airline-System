from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Flight, Booking, Passenger, Airport


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
        user = User.objects.get(username=obj['username'])
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "username" and "password".',
                code='authorization'
            )

        attrs['user'] = user
        return attrs

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

class BookingSerializer(serializers.ModelSerializer):
    # passenger = PassengerSerializer()
    flight = FlightSerializer()
    class Meta:
        model = Booking
        fields = ['id', 'passenger', 'flight', 'booking_code', 'user']