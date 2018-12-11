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
    #重写RegistrationView类。。如果把一个类作为视图，最后要写成 .as_view()方法
    url(r'^accounts/register/$', views.RangoRegistrationView.as_view(), name='registration_register'),

    #导入这个registration外部应用，它内部写好了视图函数，我们需要自己写模板
    url(r'^accounts/',include('registration.backends.simple.urls')),#引入 registration 包的URL 映射

    url(r'^users/',include('users.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
