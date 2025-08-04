from django.contrib import admin
from .models import EmailOTP

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'created_at', 'is_verified')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('email',)
    readonly_fields = ('created_at',)
    
    def has_add_permission(self, request):
        """Disable manual addition of OTPs"""
        return False
