from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, re_path, path

admin.autodiscover()

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)