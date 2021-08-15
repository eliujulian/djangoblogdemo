"""djangoblogdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from blog.views import *


urlpatterns = [
    path('', BlogView.as_view(), name="landingpage"),
    path('article/create/', ArticleCreateView.as_view(), name="article-create"),
    path('article/<slug>/', ArticleDetailView.as_view(), name="article-detail"),
    path('article/<slug>/update/', ArticleUpdateView.as_view(), name="article-update"),
    path('article/<slug>/delete/', ArticleDeleteView.as_view(), name="article-delete"),
    path('admin/', admin.site.urls),
]
