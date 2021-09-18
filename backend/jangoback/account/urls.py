from django.urls import path
from account import views

urlpatterns = [
    # define a route for home
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
]