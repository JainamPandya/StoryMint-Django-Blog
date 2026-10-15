from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from blogs.models import Blog, Category, Tag, UserProfile
from .forms import BlogPostForm, CategoryForm, TagForm, UserProfileForm, UserEditForm

@login_required
def dashboard(request):
    if request.user.is_superuser:
        posts = Blog.objects.all().order_by('-created_at')
    else:
        posts = Blog.objects.filter(author=request.user).order_by('-created_at')

    posts_count = posts.count()
    published_count = posts.filter(status='Published').count()
    drafts_count = posts.filter(status='Draft').count()
    total_views = sum(post.views_count for post in posts)
    total_likes = sum(post.total_likes() for post in posts)

    # User's bookmarked posts
    bookmarked_posts = request.user.bookmarked_blogs.filter(status='Published').order_by('-created_at')

    context = {
        'posts': posts,
        'posts_count': posts_count,
        'published_count': published_count,
        'drafts_count': drafts_count,
        'total_views': total_views,
        'total_likes': total_likes,
        'bookmarked_posts': bookmarked_posts,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            base_slug = slugify(post.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post.slug = slug
            post.save()
            form.save_m2m() # Saves tags
            messages.success(request, 'Article published successfully!')
            return redirect('dashboard')
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_post.html', context)


@login_required
def edit_post(request, slug):
    if request.user.is_superuser:
        post = get_object_or_404(Blog, slug=slug)
    else:
        post = get_object_or_404(Blog, slug=slug, author=request.user)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'dashboard/edit_post.html', context)


@login_required
def delete_post(request, slug):
    if request.user.is_superuser:
        post = get_object_or_404(Blog, slug=slug)
    else:
        post = get_object_or_404(Blog, slug=slug, author=request.user)

    post.delete()
    messages.success(request, 'Article deleted successfully!')
    return redirect('dashboard')


# Category Management
@login_required
def categories(request):
    categories_list = Category.objects.all().order_by('category_name')
    context = {
        'categories_list': categories_list,
    }
    return render(request, 'dashboard/categories.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('categories')
    else:
        form = CategoryForm()

    context = {'form': form}
    return render(request, 'dashboard/category_form.html', context)


@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    context = {'form': form, 'category': category}
    return render(request, 'dashboard/category_form.html', context)


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories')


# Tag Management
@login_required
def tags(request):
    tags_list = Tag.objects.all().order_by('name')
    context = {
        'tags_list': tags_list,
    }
    return render(request, 'dashboard/tags.html', context)


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag added successfully!')
            return redirect('tags')
    else:
        form = TagForm()

    context = {'form': form}
    return render(request, 'dashboard/tag_form.html', context)


@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    messages.success(request, 'Tag deleted successfully!')
    return redirect('tags')


# Profile Settings
@login_required
def profile_settings(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_settings')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'dashboard/profile_settings.html', context)
