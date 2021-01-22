from django.urls import path
from litBlog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', auth_views.LoginView.as_view()),
    path('flux/', views.flux, name="flux"),

    path('ticket/', views.ticket, name='ticket'),
    path('ticket/<int:id_ticket>', views.ticket, name='ticket'),
    path('delete_ticket/<int:id_ticket>', views.delete_ticket, name='delete_ticket'),

    path('post/', views.post, name='post'),

]
