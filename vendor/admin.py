from django.contrib import admin
from .models import EmailOTP, Document


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp', 'created_at', 'is_verified']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """Disable manual OTP creation for security"""
        return False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_type', 'filename', 'uploaded_at', 'is_verified', 'file_size_mb']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['uploaded_at', 'file_size_mb']
    ordering = ['-uploaded_at']
    
    def filename(self, obj):
        """Display filename"""
        return obj.filename()
    filename.short_description = 'Filename'
    
    def file_size_mb(self, obj):
        """Display file size in MB"""
        return f"{obj.file_size_mb()} MB"
    file_size_mb.short_description = 'File Size'
