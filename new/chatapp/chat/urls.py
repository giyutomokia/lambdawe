from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.chat_home, name='chat_home'),  # Chat homepage
    path('chat/<int:user_id>/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
]
