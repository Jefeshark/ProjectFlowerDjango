from django.contrib import admin

from .models import User, Category, Flowers, Order, OrderTime


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...

@admin.register(Flowers)
class FlowersAdmin(admin.ModelAdmin):
    ...

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ...

@admin.register(OrderTime)
class OrderTimeAdmin(admin.ModelAdmin):
    ...

