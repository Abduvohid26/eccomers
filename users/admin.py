from django.contrib import admin
from .models import User, UserConfirmation

class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = ('username', 'user_roles', 'phone_number')


admin.site.register(User, UserAdmin)
admin.site.register(UserConfirmation)