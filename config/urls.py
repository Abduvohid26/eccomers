from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('users/api/sxema', SpectacularAPIView.as_view(), name='sxema'),
    path('users/api/sxema/redoc', SpectacularRedocView.as_view(url_name='sxema'), name='redoc'),
    path('users/api/sxema/swagger', SpectacularSwaggerView.as_view(url_name='sxema'), name='swagger'),
]
