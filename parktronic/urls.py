from django.contrib import admin
from django.urls import path, include
from web_app import views
from web_app import urls as api_urls
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view()),
    path('token/', obtain_auth_token),
    path('api/', include(api_urls, namespace='web_app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 