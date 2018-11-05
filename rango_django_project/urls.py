from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from rango import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    #下面的映射把以rango/开头的URL交给rango的应用处理
    url(r'^rango/',include('rango.urls')),
    url(r'^users/',include('users.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
