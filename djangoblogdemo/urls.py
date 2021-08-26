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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', BlogView.as_view(), name="landingpage"),
    path('login/', LoginView.as_view(template_name="blog/login.html"), name="login"),
    path('logout/', LogoutView.as_view(template_name="blog/login.html"), name="logout"),
    path('register/', AccountRegisterView.as_view(), name="register"),
    path("account/", login_required(AccountDetailView.as_view()), name="account-detail"),
    path('imprint/', ImprintView.as_view(), name="imprint"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('privacy/', PrivacyView.as_view(), name="privacy"),
    path('article/list/', login_required(ArticleListView.as_view()), name="article-list"),
    path('article/create/', login_required(ArticleCreateView.as_view()), name="article-create"),
    path('article/<slug>/', ArticleDetailView.as_view(), name="article-detail"),
    path('article/<slug>/update/', login_required(ArticleUpdateView.as_view()), name="article-update"),
    path('article/<slug>/delete/', login_required(ArticleDeleteView.as_view()), name="article-delete"),
    path('article/<slug>/new_comment/', login_required(BlogCommentCreateView.as_view()), name="blog-comment-create"),
    path('comment/<slug>/update/', login_required(BlogCommentUpdateView.as_view()), name="blog-comment-update"),
    path('admin/', admin.site.urls),
]
