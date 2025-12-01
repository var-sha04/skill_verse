from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('main/', views.main_view, name='main'),
    path('profile/', views.profile_view, name='profile'),
    path('discover_skills/', views.discover_skills_view, name='discover_skills'),
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('create_profile/', views.create_profile_view, name='create_profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('discover_skills_explore/', views.discover_skills_explore, name='discover_skills_explore'),
    path('profile/<int:profile_id>/', views.view_other_profile, name='view_other_profile'),
    path('messages/', views.messages_view, name='messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('chat/<str:username>/', views.chat_view, name='chat'),

    path('search_users/', views.search_users, name='search_users'),
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/edit/', views.edit_faculty, name='edit_faculty'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('admin-login/', views.admin_login_view, name='admin_login'),

    
]
