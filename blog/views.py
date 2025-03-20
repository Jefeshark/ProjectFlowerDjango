from django.shortcuts import render
from django.http import HttpResponse

from blog.models import User, Category, Flowers, Order, OrderTime

def index(request):
    users = User.objects.all()
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'users': users,
    }

    return render(
        request,
        'blog/index.html',
        context,
    )