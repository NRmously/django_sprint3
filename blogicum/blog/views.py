from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.timezone import now

from .models import Post, Category


def filters():
    return Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )


def index(request: HttpResponse) -> HttpResponse:
    posts = filters()
    template = 'blog/index.html'
    context = {'post_list': posts[0:5]}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(filters(), id=id)
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category: str) -> HttpResponse:
    post_list = get_list_or_404(
        Post.objects.select_related(
            'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=now(),
            category__slug=category
        )
    )
    category = Category.objects.values('title', 'description').get(
        slug=category
    )
    template = 'blog/category.html'
    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
