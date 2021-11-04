from django.contrib import admin
from .models import DetailOfUser, Subdivision, Position

admin.site.register(Subdivision)
admin.site.register(DetailOfUser)
admin.site.register(Position)