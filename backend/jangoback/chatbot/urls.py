from django.urls import path
from chatbot import views
urlpatterns = [
    # define a route for home
    path('chat',views.chat, name='chat')
]