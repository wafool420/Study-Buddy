from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register"),
    path('', views.home, name="home"),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
    path('post/<int:post_id>/comments/', views.comment_section, name='comment_section'),

]
