from django.urls import path
from litBlog import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', auth_views.LoginView.as_view()),

    path('flux/', views.flux, name="flux"),

    path('post/', views.post, name='post'),
    path('post_following_user/', views.post_user_following, name='post_following_user'),

    path('ticket/', views.ticket, name='ticket'),
    path('ticket/<int:id_ticket>', views.ticket, name='ticket'),
    path('delete_ticket/<int:id_ticket>', views.delete_ticket, name='delete_ticket'),

    path('review/', views.review, name='review'),
    path('review/<int:id_ticket>', views.review, name='review'),
    path('review/<int:id_ticket>/<int:id_review>', views.review, name='update_review'),
    path('delete_review/<int:id_review>', views.delete_review, name='delete_review'),

    path('own_review', views.own_review, name='own_review'),

    path('abonnements/', views.follow, name='abonnements'),
    path('abonnements/<int:id_follow>', views.delete_follow, name='delete_follow'),
]
