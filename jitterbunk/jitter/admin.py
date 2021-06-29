from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Bunk

class UserAdmin(BaseUserAdmin):
   fieldsets = (
       (None, {'fields': ('username', 'password', )}),
       (('Personal info'), {'fields': ('first_name', 'last_name', 'photo')}),
       (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
   )

   list_display = ['username', 'first_name', 'last_name', 'is_staff', 'date_joined', 'num_bunks']
   search_fields = ('email', 'first_name', 'last_name')
   ordering = ('username', )
admin.site.register(User, UserAdmin)
admin.site.register(Bunk)