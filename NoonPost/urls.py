from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
<<<<<<< HEAD
from django.conf.urls.static import static
=======
>>>>>>> Profile
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('AccountApp.urls')),
<<<<<<< HEAD
    path('', include('BlogApp.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
    path('profile/', include('ProfileApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> Profile
