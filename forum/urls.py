from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.ForumMainView.as_view(), name='forum_main'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug:slug>/new_thread/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('thread/<slug:slug>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/<slug:thread_slug>/add_post/', views.add_post, name='add_post'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('user/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('inbox/', views.inbox, name='inbox'),
    path('send_message/', views.send_message, name='send_message'),
    path('send_message/<str:username>/', views.send_message, name='send_message_with_username'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('check-key/', views.check_key, name='check_key'),
    path('post/like/', views.like_post, name='like_post'),
]
