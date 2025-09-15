from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('admin-site/', admin.site.urls),
  re_path(r'^accounts/', include('accounts.urls')),
  re_path(r'^aula_virtual/', include('aula_virtual.urls')),
  re_path(r'^', include('main.urls')),
  re_path(r'^calendario/', include('fullcalendar.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
