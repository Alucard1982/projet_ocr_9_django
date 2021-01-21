from django.urls import path
from litBlog import views

urlpatterns = [
    path('flux/', views.flux, name="flux"),

]
