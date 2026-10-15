from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from blogs import views as BlogsView
from blogs.feeds import LatestPostsFeed
from django.contrib.sitemaps.views import sitemap
from blogs.sitemaps import BlogSitemap, CategorySitemap

sitemaps = {
    'blogs': BlogSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('category/', include('blogs.urls')),
    path('tag/<slug:slug>/', BlogsView.posts_by_tag, name='posts_by_tag'),
    path('author/<str:username>/', BlogsView.author_profile, name='author_profile'),
    path('blogs/search/', BlogsView.search, name='search'),
    path('blogs/<slug:slug>/', BlogsView.blogs, name='blogs'),
    path('blogs/<slug:slug>/comment/', BlogsView.add_comment, name='add_comment'),
    path('blogs/<slug:slug>/like/', BlogsView.like_blog, name='like_blog'),
    path('blogs/<slug:slug>/bookmark/', BlogsView.bookmark_blog, name='bookmark_blog'),
    path('newsletter/subscribe/', BlogsView.subscribe_newsletter, name='subscribe_newsletter'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    ## dashboards
    path('dashboard/', include('dashboards.urls')),
    path('<slug:slug>/', BlogsView.blogs, name='blog_detail_fallback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
