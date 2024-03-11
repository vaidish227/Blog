from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [

       #API to post the comment
    path('postComment', views.postComment, name="postComment"),
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),
]
