from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "experience_level",
        "focus_area",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "experience_level",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "focus_area",
    )

    ordering = (
        "username",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile Information",
            {
                "fields": (
                    "bio",
                    "profile_picture",
                    "experience_level",
                    "focus_area",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Profile Information",
            {
                "fields": (
                    "email",
                    "experience_level",
                    "focus_area",
                )
            },
        ),
    )