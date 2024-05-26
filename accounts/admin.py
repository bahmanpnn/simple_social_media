from django.contrib import admin
from .models import RelationUser,ProfileUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


admin.site.register(RelationUser)
# admin.site.register(ProfileUser)

class ProfileUserInline(admin.StackedInline):
    model=ProfileUser
    can_delete=False

class ExtendedUserAdmin(UserAdmin):
    inlines=(ProfileUserInline,)

admin.site.unregister(User)
admin.site.register(User,ExtendedUserAdmin)
