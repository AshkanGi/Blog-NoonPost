from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('AccountApp.urls')),
    path('', include('BlogApp.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('profile/', include('ProfileApp.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




