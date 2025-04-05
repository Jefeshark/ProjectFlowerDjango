# urls.py (без изменений)
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import *

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('flower/<int:flower_id>/', flower_id, name='flower_detail'),
    path('login/', login_view, name='login'),  
    path('registration/', reg_view, name='registration'),  
    path('logout/', logout, name='logout'), 
    path('basket/', basket, name='basket'),
    path('add_basket/', add_basket, name='add_basket'),
    path('update_quantity/', update_quantity, name='update_quantity'),
    path('remove_from_basket/<int:item_id>/', remove_from_basket, name='remove_from_basket'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)