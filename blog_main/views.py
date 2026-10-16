from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from blogs.models import Category, Blog, Tag
from .forms import RegistrationForm

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('-updated_at')
    
    # Recent posts with pagination (6 per page)
    all_posts = Blog.objects.filter(is_featured=False, status='Published').order_by('-created_at')
    paginator = Paginator(all_posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Trending / Popular posts
    trending_posts = Blog.objects.filter(status='Published').order_by('-views_count')[:4]
    
    # Popular Tags
    popular_tags = Tag.objects.all()[:15]

    context = {
        'categories': categories,
        'featured_posts': featured_posts,
        'posts': posts,
        'trending_posts': trending_posts,
        'popular_tags': popular_tags,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_page = request.POST.get('next') or next_url
                if next_page and next_page != 'home':
                    return redirect(next_page)
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'next': next_url,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /dashboard/",
        "Disallow: /admin/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")