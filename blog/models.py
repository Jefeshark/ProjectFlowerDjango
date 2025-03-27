from django.db import models

class User(models.Model):
    first_name = models.CharField(
        verbose_name='имя',
        max_length=255,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=255,
    )
    email = models.EmailField(
        verbose_name='почта',
        max_length=255,
        unique=True,
    )
    password = models.CharField(
        verbose_name='пароль',
        max_length=255,
    )
    address = models.TextField(
        verbose_name='адрес доставки',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Category(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=500,
    )

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Flowers(models.Model):
    title = models.CharField(
        verbose_name='название',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='описание',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(
        verbose_name='количество в наличии',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )
    date_add = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата добавления',
    )
    image = models.ImageField(
        verbose_name='картинки',
        upload_to='uploads/',
    )
    image_two = models.ImageField(
        verbose_name='вторая картинка',
        upload_to='uploads/',
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'цветок'
        verbose_name_plural = 'цветы'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    order_date = models.DateTimeField(
        verbose_name='дата',
        auto_now_add=True,
    )
    status_choices = [
        ('processing', 'в обработке'),
        ('shipped', 'отправлен'),
        ('delivered', 'доставлен'),
        ('canceled', 'отменен'),
    ]
    status_order = models.CharField(
        max_length=20,
        choices=status_choices,
        default='processing',
        verbose_name='статус заказа',
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='общая сумма',
    )

    def add_flower(order, flower, quantity):
        order_time = OrderTime(
            order=order,
            flower=flower,
            quantity=quantity,
            unit_price = flower.price
        )

        order_time.save()
        order.add_flower()


    def __str__(self):
        return f"Заказ {self.id} от {self.user}"


    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderTime(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='заказ',
    )
    flower = models.ForeignKey(
        Flowers,
        on_delete=models.CASCADE,
        verbose_name='цветок',
    )
    quantity = models.DecimalField(
        verbose_name='количество',
        max_digits=10,  
        decimal_places=2,  
    )
    unit_price = models.DecimalField(
        verbose_name='цена за единицу',
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.flower.title} - {self.quantity} шт."
    
    class Meta:
        verbose_name = 'позиция'
        verbose_name_plural = 'позиции'


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Flowers,
        on_delete=models.CASCADE,   
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='количество'
    )
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Корзина для {self.user} | Товар {self.product}"

    
    class Meta:
        verbose_name = 'корзина'


