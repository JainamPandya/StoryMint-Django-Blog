from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Blog

class LatestPostsFeed(Feed):
    title = "StoryMint - Latest Blog Posts"
    link = "/"
    description = "Updates on new stories and articles published on StoryMint."

    def items(self):
        return Blog.objects.filter(status='Published').order_by('-created_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_link(self, item):
        return reverse('blogs', kwargs={'slug': item.slug})

    def item_pubdate(self, item):
        return item.created_at
