from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog.views import index, flower_id, login_view, logout, reg_view

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('flower/<int:flower_id>/', flower_id, name='flower_detail'),
    path('login/', login_view, name='login_view'),  
    path('registration/', reg_view, name='reg_view'),  
    path('logout/', logout, name='logout'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)