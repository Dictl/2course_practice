from django.urls import path
from . import views
from .views import profile_edit_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('profile/delete/', views.delete_account_view, name='delete_account'),

]