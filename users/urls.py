from users import views

from django.conf.urls import url

app_name='users'#创建了命名空间
urlpatterns = [
 url('^register/$',views.register,name="register"),
 url('^login/$',views.user_login,name='login'),
 url('^logout/$',views.user_logout,name='logout'),
]