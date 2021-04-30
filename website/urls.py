from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('inbox/', views.inbox, name="inbox"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('share/', views.share, name="share"),
    path('delete-message/', views.deleteMessage, name="deleteMessage"),
    path('delete-account/', views.deleteAccount, name="deleteAccount"),
]
