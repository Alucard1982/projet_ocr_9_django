from django.urls import path
from blog import views

urlpatterns = [
    path('flux/', views.flux, name="flux"),

]
