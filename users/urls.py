from users import views

from django.conf.urls import url

app_name='users'#创建了命名空间
urlpatterns = [
 url('^register/$',views.register,name="register"),
]