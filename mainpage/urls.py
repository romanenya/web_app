from django.urls import path
from . import views

urlpatterns = [
    path('list_of_users', views.list_of_users),
    path('positions', views.positions),
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('add_user', views.add_user),
    path('my_card', views.my_card),
    path('add_subdivision', views.add_subdivision)
]