from django.urls import path
from web_app import views

urlpatterns = [
    path('cars/', views.cars_list),
    path('cars/<int:pk>/', views.car_detail),
    path('persons/', views.person_list),
    path('persons/<int:pk>/', views.person_detail)
]
