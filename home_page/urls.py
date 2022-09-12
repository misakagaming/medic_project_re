from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='hospital-home'),
    path('user/<username>', views.UserNewsView.as_view(), name='user-news'),
    path('news/<int:pk>/', views.NewsDetailsView.as_view(), name='news-detail'),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news-delete'),
    path('news/new/', views.NewsCreateView.as_view(), name='news-create'),
    path('about/', views.AboutView.as_view(), name='hospital-about'),
]
