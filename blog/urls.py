from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path("connect/", views.LecteurRegister.as_view(), name="lecteur_register"),
    path("<int:pk>/",views.ArticleDetailView.as_view(), name='article_detail'),
    path("",views.ArticleListView.as_view(), name='article_list'),
]