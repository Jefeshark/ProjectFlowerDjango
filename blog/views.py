from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from blog.models import User, Category, Flowers, Order, OrderTime

def index(request):
    categories = Category.objects.all()
    flowers = Flowers.objects.all()

    context = {
        'flowers': flowers,
        'categories': categories,
        'SETTINGS': settings,
    }

    return render(
        request,
        'blog/index.html',
        context,
    )

