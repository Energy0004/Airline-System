from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Airport, Flight, Passenger, Booking

# admin.site.register(User, UserAdmin)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Booking)