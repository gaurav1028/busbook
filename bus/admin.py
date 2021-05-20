from django.contrib import admin
from .models import *

admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(BusStop)
admin.site.register(Schedule)
admin.site.register(Ticket)
admin.site.register(PassengerDetail)