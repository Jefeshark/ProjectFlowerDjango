from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from blog.models import Category, Flowers

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
    }
    return render(request, 'blog/flower_detail.html', context)

def reg_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'auth/reg.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'auth/reg.html')

        try:
            user = User.objects.create_user(username=username, password=password)
            auth_login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'Ошибка при регистрации: {str(e)}')
            return render(request, 'auth/reg.html')

    return render(request, 'auth/reg.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Вы успешно вошли в систему')
            return redirect('index')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'auth/login.html')
    
    return render(request, 'auth/login.html')

def logout(request):
    auth_logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('login_view')