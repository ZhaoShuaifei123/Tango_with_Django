from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rango import views

from rango import views

app_name='rango'#创建了命名空间
urlpatterns = [
     url(r'^about/$',views.about,name='about'),
     url(r'^show_category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name='show_category'),
     url(r'^add_category/$',views.add_category,name='add_category'),
     url(r'^add_page/(?P<category_name_slug>[\w\-]+)/$',views.add_page,name="add_page"),
     url(r'^search/$',views.search,name='search'),
     url(r'^like/$',views.like_category,name='like_category'),
     url(r'^suggestion/$',views.suggest_category,name="suggestion"),
]
