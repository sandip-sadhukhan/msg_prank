from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('inbox/', views.inbox, name="inbox"),
    path('login/', views.login, name="login"),
]
