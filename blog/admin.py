from django.contrib import admin
from django import forms

from .models import Article, Author, Comments, Category

from ckeditor_uploader.widgets import CKEditorUploadingWidget



class BlogAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'



class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    form = BlogAdminForm


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
