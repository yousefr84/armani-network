"""
URL configuration for Armani_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from armani import views
from armani.views import UserDetailAPIView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/mentors/', views.MentorListAPIView.as_view()),
    # path('api/projects/', views.ProjectListAPIView.as_view()),
    # path('api/article/', views.ArticleListAPIView.as_view()),
    path('api/user-detail/', UserDetailAPIView.as_view(), name='user-detail'),
    # path('api/mentor/', views.MentorsDetailAPIView.as_view()),
    path('api/register/', views.RegisterAPIView.as_view()),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/select2/', include('django_select2.urls')),
    path('api/project/', views.ProjectDetailAPIView.as_view()),
    path('api/article/', views.ArticleDetailAPIView.as_view()),
    path('api/main/', views.MainListAPIView.as_view()),
    path('api/services/', views.ServicesListAPIView.as_view()),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
