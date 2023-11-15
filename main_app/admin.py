from django.contrib import admin
import main_app.models as _models
from django.contrib.auth.admin import UserAdmin
from main_app.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
# Register your models here

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'name', 'apellidos',
                    'is_staff',)
    list_filter = ('is_staff',)
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'apellidos',
         'email', 'password',)}),
        ('Permissions', {
         'fields': ('groups', 'user_permissions',)}),
        ('Types', {'fields': ('is_staff',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'apellidos', 'groups', 'user_permissions', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
