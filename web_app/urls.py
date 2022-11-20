from django.urls import path
from web_app import views

from .views import LoginAPIView, RegistrationAPIView


app_name = "web_app"
urlpatterns = [
    path('cars/', views.cars_list),
    path('cars/<int:pk>/', views.car_detail),
    path('car/create/', views.create_car),
    path('persons/', views.person_list),
    path('person/<int:pk>/', views.person_detail),
    path('person/create/', views.create_person),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('file/uplode/', views.PtsStsUploadView.as_view()),
]
