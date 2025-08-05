from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# drf-yasg imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_info = openapi.Info(
    title="Vendor Django REST API",
    default_version='v1',
    description="API documentation for Vendor Django REST API with OTP authentication, user management, and document upload.",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="support@vendorapp.local"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendor/', include('vendor.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
