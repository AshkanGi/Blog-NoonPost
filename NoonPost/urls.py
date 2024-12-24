from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('AccountApp.urls')),
    path('profile/', include('ProfileApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
