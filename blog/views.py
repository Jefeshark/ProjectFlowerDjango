from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from blog.models import Category, Flowers, Basket

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
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from blog.models import Flowers, Basket

def basket(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    basket_items = Basket.objects.filter(user=user)
    total_price = sum(item.product.price * item.quantity for item in basket_items)
    
    context = {
        'basket_items': basket_items,
        'total_price': total_price,
    }
    return render(request, 'blog/basket.html', context)

def add_basket(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        product_id = request.POST.get('flower_id')
        user = request.user
        
        try:
            product = Flowers.objects.get(id=product_id)
            
            if product.stock < 1:
                messages.error(request, 'Этот цветок закончился в наличии')
                return redirect(request.META.get('HTTP_REFERER', 'index'))
            
            basket_item, created = Basket.objects.get_or_create(
                product=product,
                user=user,
                defaults={'quantity': 1}
            )
            
            if not created:
                if basket_item.quantity >= product.stock:
                    messages.error(request, 'Достигнуто максимальное количество для этого цветка')
                    return redirect('basket')
                basket_item.quantity += 1
                basket_item.save()
                
            messages.success(request, 'Товар добавлен в корзину')
        except Flowers.DoesNotExist:
            messages.error(request, 'Товар не найден')
            
    return redirect('basket')

def update_quantity(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        try:
            basket_item = Basket.objects.get(id=item_id, user=request.user)
            product = basket_item.product
            
            if action == 'increase':
                if basket_item.quantity >= product.stock:
                    messages.error(request, 'Недостаточно товара на складе')
                else:
                    basket_item.quantity += 1
                    basket_item.save()
            elif action == 'decrease':
                if basket_item.quantity > 1:
                    basket_item.quantity -= 1
                    basket_item.save()
                else:
                    basket_item.delete()
            return redirect('basket')
        except Basket.DoesNotExist:
            pass
            
    return redirect('basket')

def remove_from_basket(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    basket_item = get_object_or_404(Basket, id=item_id, user=request.user)
    basket_item.delete()
    
    return redirect('basket')