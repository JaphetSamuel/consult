from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    path('register/', views.register_author, name='register'),
]