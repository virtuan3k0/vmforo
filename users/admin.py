from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'subscription_status', 'forum_messages')  # Added forum_messages
    list_filter = ('is_staff', 'is_active', 'subscription_status')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'avatar', 'bio')}),
        ('Subscription', {'fields': ('subscription_status', 'subscription_start_date', 'subscription_end_date', 'is_trial_used', 'is_auto_renewal')}),
        ('Stripe Info', {'fields': ('stripe_customer_id', 'stripe_subscription_id')}),
        ('Educational Info', {'fields': ('educational_status', 'desired_specialty')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
