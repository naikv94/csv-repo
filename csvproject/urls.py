from django.contrib import admin
from django.urls import path
from api import views
from csvproject import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.upload_file, name='index'),
    path('getdata/', views.getData, name='getdata'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)