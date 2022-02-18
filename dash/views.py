from django.shortcuts import render
from blog.models import Article, Category, Comments, Author
from django.views import generic
from django.contrib.auth import authenticate, login, forms, models as auth_models
from django.http import HttpResponse


# Create your views here.
def register_author(request):
    form = forms.UserCreationForm()


    if request.method == 'POST':
        username = request.POST['username']
        raw_password = request.POST['password1']
        email = request.POST['email']
        user = auth_models.User(username=username, email=email, is_active=False)
        user.set_password(raw_password)
        user.save()
        Author(user=user).save()

        return HttpResponse(f"<h1>Un mail de confirmation a été envoyé a l'adresse {email} </h1>")
    

    return render(request, 'dash/signup_.html', {'form': form})