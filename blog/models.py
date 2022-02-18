
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def send_confirmation_email(self):
        if self.user.is_active:
            return
        link = "http://localhost:8000/dash/confirm/{}".format(self.user.username)
        send_mail(
            subject="Confirmez votre compte",
            from_email="consultadmin@gmail.com",
            recipient_list=[self.user.email],
            html_message=f"""
            <h1>Bienvenue sur le blog de la Consult</h1>
            <p>Merci de confirmer votre compte en cliquant sur le lien suivant:</p>
            <a href="{link}>Confirmer</a>
            """
        )
        
        

    def __str__(self):
        return self.user.username

class Lecteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    paid_article = models.ManyToManyField('Article', blank=True)


    def send_confirmation_email(self):
        if self.user.is_active:
            return
        link = "http://localhost:8000/dash/confirm/{}".format(self.user.username)
        send_mail(
            subject="Confirmez votre compte",
            from_email="consultadmin@gmail.com",
            recipient_list=[self.user.email],
            html_message=f"""
            <h1>Bienvenue sur le blog de la Consult</h1>
            <p>Merci de confirmer votre compte en cliquant sur le lien suivant:</p>
            <a href="{link}>Confirmer</a>
            """
        )
    
    def send_payment_confirmed_email(self):
        send_mail(
            subject="Votre paiement a été confirmé",
            from_email="noreply@consult.com",
            recipient_list=[self.user.email],
            html_message=f"""
            bonjour {self.user.username},
            <h1>Votre paiement a été confirmé</h1>
            
            """
        )

    def __str__(self):
        return self.user.username


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name="titre")
    cover = models.ImageField(upload_to='cover_pics', blank=True)
    body = RichTextUploadingField(blank=True, verbose_name="contenu")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="auteur")
    date = models.DateTimeField(auto_now_add=True)
    identifiant = models.UUIDField(default=uuid.uuid4, editable=False)
    like = models.PositiveIntegerField(default=0)
    category = models.ManyToManyField('Category', blank=True)

    for_sale = models.BooleanField(default=False)
    price = models.IntegerField(default=0)

    @property
    def author_name(self):
        return self.author.user.username

    def payement(self, lecteur:Lecteur):
        if self.for_sale:
            #processus de payement
            lecteur.paid_article.add(self)


    def __str__(self):
        return self.title





class Comments(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.body
    
    @property
    def author_name(self):
        return self.author.username
    
    @property
    def author_pp(self):
        if self.author.author.profile_picture is not None:
            return self.author.author.profile_picture
        else :
            return self.author.lecteur.profile_picture

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
