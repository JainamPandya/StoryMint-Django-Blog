from django.shortcuts import redirect, render,get_object_or_404
from django.http import Http404, HttpResponse
from . models import Blog,Category
from django.db.models import Q

def posts_by_category(request, category_id):
    try:
        category = get_object_or_404(Category, pk=category_id)
    except:
        return redirect('home')
    posts = Blog.objects.filter(
        category=category,
        status="Published", 
    ).order_by("-created_at")

    return render(request, "category_posts.html", {
        "category": category ,
        "posts": posts,
    })


def blogs(request, slug):
    single_blog = get_object_or_404(Blog,slug=slug,status='Published')
    context = {
        'single_blog' : single_blog ,
    }    
    return render(request, 'blogs.html',context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword)|Q(short_description__icontains=keyword)|Q(blog_body__icontains=keyword),status='Published')
    context = {
        'blogs' : blogs,
        'keyword' : keyword,
    }
    return render(request, "search.html",context)