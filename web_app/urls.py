from django.urls import path
from web_app import views

urlpatterns = [
    path('cars/', views.cars_list),
]
