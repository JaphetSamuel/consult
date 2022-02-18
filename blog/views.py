
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .models import Article, Lecteur
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import models as auth_models, authenticate, login

# Create your views here.
class ArticleListView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    #handing filter query
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            query = request.POST.get('search')
            if query:
                article_list = Article.objects.filter(title__icontains=query)
                return render(request, 'blog/index.html', {'article_list': article_list})
        else:
            return render(request, 'blog/index.html')


class ArticleDetailView(generic.DetailView, LoginRequiredMixin):
    model = Article
    template_name = 'blog/article.html'
    login_url=reverse_lazy("blog:lecteur_register")

    def get(self, request, *args, **kwargs):
        if self.get_object().for_sale:
            return render(request, template_name='blog/article_detail.html')
        
        return super().get(request, *args, **kwargs)
    

def pay(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.payement(lecteur = request.user.lecteur)
    
    return redirect('dash:article_detail', {'pk':article_id})

class LecteurRegister(generic.View):
    def post(self, request,*args, **kwargs):
        username = request.POST['username']
        raw_password = request.POST['password1']
        email = request.POST['email']
        user = auth_models.User(username=username, email=email, is_active=False)
        user.set_password(raw_password)
        user.save()
        Lecteur(user=user).save()
        return HttpResponse(f"<h1>Un mail de confirmation a été envoyé a l'adresse {email} </h1>")
    

def lecteur_connect(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)




