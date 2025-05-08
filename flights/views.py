import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *



class UserAPIRegistration(APIView):
    def post(self, request):
        if User.objects.filter(email=request.data['email']).exists():
            raise serializers.ValidationError({"email": ["A user with that email already exists."]})
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            return Response({
                'user': UserSerializer(user).data,
                'tokens': serializer.get_tokens(user),
                'message': 'User created successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPILogin(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                'user': UserSerializer(user).data,
                'tokens': serializer.get_tokens(serializer.validated_data)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPILogout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserAPIProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# class UsersAPIList(generics.ListAPIView)
#     permission_classes = [IsAuthenticated]

class UserAPIUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAPIUser(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'User account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class ChangePasswordAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response({"password": ["Both password fields are required."]}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"password": ["Passwords do not match."]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


class FlightAPIList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # permission_classes = [permissions.AllowAny]

class FlightAPIDetails(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # permission_classes = [permissions.AllowAny]

# class AirportAPIList(generics.ListAPIView):
#     queryset = Airport.objects.all()
#     serializer_class = AirportSerializer

class AirportAPIDetails(generics.RetrieveAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    def get(self, request, *args, **kwargs):
        airport = self.get_object()

        departures = airport.departures.all()
        arrivals = airport.arrivals.all()

        airport_data = self.get_serializer(airport).data
        departures_data = FlightSerializer(departures, many=True).data
        arrivals_data = FlightSerializer(arrivals, many=True).data

        return Response({
            'airport': airport_data,
            'departures': departures_data,
            'arrivals': arrivals_data
        })

class MyBookingAPIDetails(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)

class BookingAPIConfirmation(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCodeSerializer

class BookingAPICreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        flight_id = request.data.get('flight_id')

        if not flight_id:
            return Response(
                {"error": "Missing required field \'flight_id\'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            flight = get_object_or_404(Flight, pk=flight_id)

            name = request.data.get("username")
            email = request.data.get("email")
            existing_booking = Booking.objects.filter(
                flight=flight,
                passenger__name=name
            ).first()
            if existing_booking:
                print("You have already booked this flight with this passenger name."),
                return Response(
                    {"error": "You have already booked this flight."},
                    status=status.HTTP_400_BAD_REQUEST
                )


            booking_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            passengers = Passenger.objects.create(name=name, email=email)
            booking = Booking.objects.create(
                passenger=passengers,
                flight=flight,
                booking_code=booking_code,
                user = request.user
            )
            flight.capacity -= 1
            flight.save()

            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class BookingAPIFind(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        code = request.data.get('code')

        if not code:
            return Response({'error': 'Booking code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if Booking.objects.filter(booking_code=code).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

class BookingAPIDetails(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    lookup_field = 'booking_code'

    def get_object(self):
        booking_code = self.kwargs.get('booking_code')
        booking = get_object_or_404(Booking, booking_code=booking_code)
        return booking

    def get(self, request, *args, **kwargs):
        try:
            booking = self.get_object()
            serializer = self.get_serializer(booking)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class AdminUserListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AdminUserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AdminBookingListAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form': form})
# def index(request):
#     flights = Flight.objects.all()
#     return render(request, 'index.html', context={
#         'flights': flights
#     })
#
# def flight(request, flight_id):
#     flights = Flight.objects.get(id=flight_id)
#     bookings = Booking.objects.filter(flight=flights)
#     return render(request, 'flight.html', context={
#         'flights': flights,
#         'bookings': bookings
#     })
#
# @login_required
# def flight_book(request, flight_id):
#     flight = Flight.objects.get(id=flight_id)
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#
#         if not name or not email:
#             return render(request, "booking.html", {
#                 "flight": flight,
#                 "error": "Name and Email cannot be empty."
#             })
#
#         passenger, create = Passenger.objects.get_or_create(name=name, email=email)
#
#         if Booking.objects.filter(passenger=passenger, flight=flight).exists():
#             return render(request, "booking.html", {
#                 "flight": flight,
#                 "error": "You have already booked this flight."
#             })
#
#         code = str(uuid.uuid4())[:6]
#         Booking.objects.create(passenger=passenger, flight=flight, booking_code=code)
#
#         flight.capacity -= 1
#         flight.save()
#         return render(request, "booking_confirmation.html", {
#             "booking_code": code
#         })
#     return render(request, "booking.html", {
#         "flight": flight
#     })
#
# @login_required
# def manage_booking(request):
#     if request.method == "POST":
#         code = request.POST.get("code")
#         if not code:
#             return render(request, "manage_booking.html", {
#                 'error': "Code cannot be empty"
#             })
#         is_code = Booking.objects.filter(booking_code=code).exists()
#         if is_code:
#             booking = Booking.objects.get(booking_code=code)
#             passenger = Passenger.objects.get(id=booking.passenger.id)
#             flight = Flight.objects.get(id=booking.flight_id)
#             return render(request, "booking_details.html", {
#                 'passenger': passenger,
#                 'booking': booking,
#                 'flight': flight
#             })
#         else:
#             return render(request, 'manage_booking.html', context={
#                 'error': 'The code is not correct'
#             })
#     return render(request, 'manage_booking.html')
#
# def airport(request, city_id):
#     airport = Airport.objects.get(id=city_id)
#     return render(request, 'airport.html', context={
#         'airport': airport,
#         'departures': airport.departures.all(),
#         'arrivals': airport.arrivals.all()
#     })