from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from blog.models import User, Category, Flowers, Order, OrderTime

def index(request):
    categories = Category.objects.all()
    flowers = Flowers.objects.all()
    
    context = {
        'categories': categories,
        'flowers': flowers,
    }
    return render(request, 'blog/index.html', context)

def flower_id(request, flower_id):
    flower = get_object_or_404(Flowers, pk=flower_id)
    additional_flower = Flowers.objects.exclude(id=flower.id).order_by('?').first()
    other_flowers = Flowers.objects.exclude(id=flower.id).order_by('?')[:8]
    context = {
        'flower': flower,
        'additional_flower': additional_flower,
        'other_flowers': other_flowers,
        'SETTINGS': settings,
    }
    return render(request, 'blog/flower_detail.html', context)