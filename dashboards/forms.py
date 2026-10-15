from django import forms
from django.contrib.auth.models import User
from blogs.models import Blog, Category, Tag, UserProfile

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'category', 'tags', 'featured_image', 'short_description', 'blog_body', 'status', 'is_featured')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'blog_body': forms.Textarea(attrs={'id': 'blog-body-editor', 'rows': 15}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture', 'website', 'twitter', 'github', 'linkedin')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
