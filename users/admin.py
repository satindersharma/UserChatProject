from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission, Group, PermissionsMixin
from .models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from django.utils.text import Truncator



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'name','email',  'is_staff',)
    # exclude = ('first_name', 'date_joined', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # the add_fieldsets allowed extra fields to be dispaly on user create form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )



admin.site.register(CustomUser, CustomUserAdmin)
