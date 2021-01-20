from django.urls import path
from login import views

urlpatterns = [
    path('sign_up/', views.sign_up, name="sign_up"),
    path('', views.login_blog, name='login'),
    path('', views.logout_blog, name='logout'),
]
