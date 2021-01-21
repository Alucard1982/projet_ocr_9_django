from django.urls import path
from litLogin import views

urlpatterns = [
    path('sign_up/', views.sign_up, name="sign_up"),
    path('home/', views.login_blog, name='login_blog'),
    path('home/', views.logout_blog, name='logout_blog'),
]
