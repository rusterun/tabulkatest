from django.contrib import admin
from .models import Bookings, Comments, Properties, Configs

admin.site.register(Bookings)
admin.site.register(Comments)
admin.site.register(Properties)
admin.site.register(Configs)
