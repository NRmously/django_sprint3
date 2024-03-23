from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.db.models.query import QuerySet

from .models import Post, Category


def is_published_filter(*args: list) -> QuerySet:
    return Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )


def index(request: HttpResponse) -> HttpResponse:
    posts = is_published_filter()
    template = 'blog/index.html'
    context = {'post_list': posts[:settings.LIMIT_OF_POSTS]}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(is_published_filter(), id=id)
    template = 'blog/detail.html'
    context = {'post': post}
    return render(request, template, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = is_published_filter().filter(category=category)
    template = 'blog/category.html'
    context = {'post_list': post_list, 'category': category}
    return render(request, template, context)
