from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('airport/<int:city_id>/', views.airport, name='airport'),
    # path('flight/<int:flight_id>/', views.flight, name='flight'),
    # path('flight/<int:flight_id>/book/', views.flight_book, name='flight_book'),
    # path('manage-booking/', manage_booking, name='manage_booking'),
    # path('register/', register, name='register'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('drf_auth/', include('rest_framework.urls')),
    path('auth/register/', UserAPIRegistration.as_view()),
    path('auth/login/', UserAPILogin.as_view()),
    path('auth/logout/', UserAPILogout.as_view()),
    path('auth/profile/', UserAPIProfile.as_view()),
    # path('users/', UsersAPIList.as_view()),
    path('users/update/me/', UserAPIUpdate.as_view()),
    path('users/change-password/', ChangePasswordAPI.as_view()),
    path('users/delete/me/', DeleteAPIUser.as_view()),
    path('flights/', FlightAPIList.as_view()),
    path('flights/<int:pk>/', FlightAPIDetails.as_view()),
    # path('airports/', AirportAPIList.as_view()),
    path('airports/<int:pk>/', AirportAPIDetails.as_view()),
    path('bookings/', BookingAPICreate.as_view()),
    path('booking-confirmation/<int:pk>', BookingAPIConfirmation.as_view()),
    path('bookings/<str:booking_code>/', BookingAPIDetails.as_view()),
    path('manage-booking/', BookingAPIFind.as_view()),
    path('my_bookings/', MyBookingAPIDetails.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('admin/users/', AdminUserListAPIView.as_view(), name='admin-user-list'),
    path('admin/users/<int:pk>/', AdminUserDetailAPIView.as_view(), name='admin-user-detail'),
    path('admin/bookings/', AdminBookingListAPIView.as_view(), name='admin-booking-list')
]