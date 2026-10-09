
from django.shortcuts import redirect, render,get_object_or_404
from django.http import Http404, HttpResponse
from . models import Blog,Category

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