from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog.views import index, flower_id

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('flower/<int:flower_id>/', flower_id, name='flower_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)