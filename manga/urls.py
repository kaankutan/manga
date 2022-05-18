"""manga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from index.views import redirect_to_language, index, manga, manga_details, manga_chapter
from index.sitemaps import MangaSitemap, StaticViewSitemap


urlpatterns = [
    path('', redirect_to_language),
    path('sitemap.xml', sitemap, {'sitemaps': {'manga': MangaSitemap}}),
    path('sitemap-static.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}),
    path('<language>/', index, name='index'),
    path('<language>/manga/', manga),
    path('<language>/manga/<manga_slug>/', manga_details),
    path('<language>/manga/<manga_slug>/<chapter_slug>/', manga_chapter),
]
