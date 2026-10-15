from django.contrib import admin
from .models import Category, Blog, Tag, Comment, UserProfile, NewsletterSubscriber

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'views_count', 'created_at')
    search_fields = ('id', 'title', 'category__category_name', 'status')
    list_editable = ('is_featured', 'status')
    filter_horizontal = ('tags',)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'created_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user__username', 'content', 'blog__title')
    list_editable = ('is_approved',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'twitter', 'github', 'created_at')

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')

admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
