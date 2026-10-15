from django.contrib.sitemaps import Sitemap
from .models import Blog, Category

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Blog.objects.filter(status='Published').order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all().order_by('id')

    def location(self, obj):
        from django.urls import reverse
        return reverse('posts_by_category', kwargs={'category_id': obj.id})
