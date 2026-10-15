from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog, Category, Tag, Comment, UserProfile, NewsletterSubscriber

def posts_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts_list = Blog.objects.filter(
        category=category,
        status="Published",
    ).order_by("-created_at")

    # Pagination: 6 posts per page
    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "category_posts.html", {
        "category": category,
        "posts": posts,
    })


def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts_list = tag.blogs.filter(status='Published').order_by('-created_at')

    paginator = Paginator(posts_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "tag_posts.html", {
        "tag": tag,
        "posts": posts,
    })


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')

    # View counter (Session based to avoid count manipulation)
    session_key = f'viewed_blog_{single_blog.id}'
    if not request.session.get(session_key, False):
        single_blog.views_count += 1
        single_blog.save(update_fields=['views_count'])
        request.session[session_key] = True

    # Related Posts (same category, excluding current post)
    related_posts = Blog.objects.filter(
        category=single_blog.category,
        status='Published'
    ).exclude(id=single_blog.id).order_by('-created_at')[:3]

    # Comments (only root level comments, replies fetched through relationship)
    comments = single_blog.comments.filter(is_approved=True, parent__isnull=True)

    # Likes & Bookmarks state for current user
    is_liked = False
    is_bookmarked = False
    if request.user.is_authenticated:
        if single_blog.likes.filter(id=request.user.id).exists():
            is_liked = True
        if single_blog.bookmarks.filter(id=request.user.id).exists():
            is_bookmarked = True

    context = {
        'single_blog': single_blog,
        'related_posts': related_posts,
        'comments': comments,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'blogs.html', context)


def add_comment(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to leave a comment.')
            return redirect('blogs', slug=slug)

        content = request.POST.get('content', '').strip()
        parent_id = request.POST.get('parent_id')

        if content:
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id, blog=single_blog).first()

            Comment.objects.create(
                blog=single_blog,
                user=request.user,
                content=content,
                parent=parent_comment
            )
            messages.success(request, 'Your comment has been posted.')
        else:
            messages.error(request, 'Comment content cannot be empty.')

    return redirect('blogs', slug=slug)


def like_blog(request, slug):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Login required'}, status=401)
        messages.warning(request, 'Please log in to like this post.')
        return redirect('blogs', slug=slug)

    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if single_blog.likes.filter(id=request.user.id).exists():
        single_blog.likes.remove(request.user)
        liked = False
    else:
        single_blog.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': single_blog.total_likes()
        })

    return redirect('blogs', slug=slug)


def bookmark_blog(request, slug):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Login required'}, status=401)
        messages.warning(request, 'Please log in to bookmark this post.')
        return redirect('blogs', slug=slug)

    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    if single_blog.bookmarks.filter(id=request.user.id).exists():
        single_blog.bookmarks.remove(request.user)
        bookmarked = False
        messages.info(request, 'Removed from your reading list.')
    else:
        single_blog.bookmarks.add(request.user)
        bookmarked = True
        messages.success(request, 'Saved to your reading list!')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'bookmarked': bookmarked,
            'total_bookmarks': single_blog.total_bookmarks()
        })

    return redirect('blogs', slug=slug)


def search(request):
    keyword = request.GET.get('keyword', '').strip()
    category_id = request.GET.get('category')

    query = Q(status='Published')
    if keyword:
        query &= (
            Q(title__icontains=keyword) |
            Q(short_description__icontains=keyword) |
            Q(blog_body__icontains=keyword) |
            Q(tags__name__icontains=keyword)
        )

    if category_id:
        query &= Q(category_id=category_id)

    blogs_qs = Blog.objects.filter(query).distinct().order_by('-created_at')

    paginator = Paginator(blogs_qs, 6)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        'blogs': blogs,
        'keyword': keyword,
        'total_results': blogs_qs.count(),
    }
    return render(request, "search.html", context)


def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=author)

    author_posts = Blog.objects.filter(author=author, status='Published').order_by('-created_at')
    paginator = Paginator(author_posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'author': author,
        'profile': profile,
        'posts': posts,
        'total_posts': author_posts.count(),
    }
    return render(request, "author_profile.html", context)


def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, 'You are already subscribed to our newsletter!')
            else:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, 'Thank you for subscribing to StoryMint newsletter!')
        else:
            messages.error(request, 'Please provide a valid email address.')

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)