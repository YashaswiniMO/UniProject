from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.forum_home, name='forum_home'),
    path('create/', views.forum_create, name='create_forum'),
    path('forums/', views.forum_list, name='forum_list'),
    path('forums/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:forum_id>/messages/', views.forum_messages, name='forum_messages'),
    path('forum/<int:forum_id>/post_message/', views.post_message, name='post_message'),
    path('forum/message/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('forum/message/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
