from django.contrib import admin
from django.urls import path
from web_app import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view()),
    path('token/', obtain_auth_token),
]
