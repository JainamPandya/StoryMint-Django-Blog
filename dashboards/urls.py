from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('posts/delete/<slug:slug>/', views.delete_post, name='delete_post'),
    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    # Tags
    path('tags/', views.tags, name='tags'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('tags/delete/<int:pk>/', views.delete_tag, name='delete_tag'),
    # Profile & Security
    path('profile/', views.profile_settings, name='profile_settings'),
    path('change-password/', views.change_password, name='change_password'),
    # Newsletter Management
    path('subscribers/', views.subscribers, name='subscribers'),
    path('subscribers/export/', views.export_subscribers_csv, name='export_subscribers_csv'),
]