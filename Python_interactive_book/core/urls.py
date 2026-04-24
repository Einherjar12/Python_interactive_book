from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.cover, name='cover'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('toc/', views.toc, name='toc'),
    path('lesson/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('submit/<slug:slug>/', views.submit, name='submit'),
    path('profile/', views.profile, name='profile'),
    path('certificate/', views.certificate, name='certificate'),
    path('certificate/verify/<str:code>/', views.verify_certificate, name='verify_certificate'),
]
