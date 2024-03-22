from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now

from .models import Post, Category


def database_querry_filter(*args: list) -> list[list]:
    return Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )


def index(request: HttpResponse) -> HttpResponse:
    posts = database_querry_filter()
    template = 'blog/index.html'
    context = {'post_list': posts[:settings.LIMIT_OF_POSTS]}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(database_querry_filter(), id=id)
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category: str) -> HttpResponse:
    post_list = database_querry_filter().filter(category__slug=category)
    category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(
            slug=category,
            is_published=True
        )
    )
    template = 'blog/category.html'
    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
