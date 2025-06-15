from django.contrib import admin
from .models.tver import TVer
from .models.member import Member

admin.site.register(TVer)
admin.site.register(Member)