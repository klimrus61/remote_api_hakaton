from django.urls import path
from web_app import views

from .views import RegistrationAPIView


app_name = "web_app"
urlpatterns = [
    path('cars/', views.cars_list),
    path('cars/<int:pk>/', views.car_detail),
    path('persons/', views.person_list),
    path('person/<int:pk>/', views.person_detail),
    path('person/', views.add_new_person),
    path('users/', RegistrationAPIView.as_view()),
]
