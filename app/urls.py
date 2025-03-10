from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from currency_converter import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/rates', views.convert, name='convert'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)