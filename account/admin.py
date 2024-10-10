from pyexpat.errors import messages
from django.conf import settings
from django.contrib import admin
import requests

# Register your models here.
from account.models import EyeImage, User, Avatar
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email","name","tc", "is_admin","mobile","country"]
    list_filter = ["is_admin"]
    fieldsets = [
        ( 'User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","tc","mobile","country"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "tc", "password1","mobile","country"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email","id"]
    filter_horizontal = ()
admin.site.register(User, UserModelAdmin)

class AvatarModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_thumbnail', 'avatar_image_url', 'created_at']
    list_filter = ['created_at'] 
    actions = ['convert_to_2d_avatar']  

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:50px;" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = 'Avatar'
admin.site.register(Avatar, AvatarModelAdmin)

admin.site.register(EyeImage)