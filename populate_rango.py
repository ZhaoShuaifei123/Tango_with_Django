import os
#DJANGO_SETTINGS_MODULE是环境变量，把DJANGO_SETTINGS_MODULE设为
# 项目的设置文件，这样调用django.setup()，会导入Django项目的设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'rango_django_project.settings')

import django
django.setup()

from rango.models import Category,Page

def populate():
    python_pages = [
        {"title": "python_pages_Official Python Tutorial",
        "url":"http://docs.python.org/2/tutorial/",
         "views":30},
        {"title": "python_pages_How to Think like a Computer Scientist",
        "url": "http://www.greenteapress.com/thinkpython/",
         "views":40},
         {"title": "python_pages_Learn Python in 10 Minutes",
          "url": "http://www.korokithakis.net/tutorials/python/",
          "views":50}]
    java_pages = [
        {"title": "java_Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views": 33},
        {"title": "java_How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 44},
        {"title": "java_Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 55}]

    c_pages = [
        {"title": "c_Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views": 33},
        {"title": "c_How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 43},
        {"title": "c_Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 53}]

    js_pages = [
        {"title": "js_Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views": 36},
        {"title": "js_How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 47},
        {"title": "js_Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 58}]

    django_pages = [
        {"title": "django_Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01xin_xin/",
         "views":60},
         {"title": "django_Django Rocks",
         "url": "http://www.djangorocks.com/",
          "views":70},
        {"title": "django_How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views":80}]

    other_pages = [
       {"title": "other_pages Bottle",
        "url":"http://bottlepy.org/docs/dev/",
        "views":90},
        {"title": "other_pages Flask",
        "url": "http://flask.pocoo.org",
         "views":100}]

    cats={"python":{"pages":python_pages,"views":120,"likes":20},
          "Django": {"pages": django_pages,"views":40,"likes":30},
          "java":{"pages":java_pages,"views":30,"likes":40},
          "c":{"pages":c_pages,"views":50,"likes":50},
          "js":{"pages":js_pages,"views":70,"likes":70},
          "Other Frameworks": {"pages": other_pages, "views": 70, "likes": 50},}

    #遍历字典时，使用cats.items()让字典变成列表
    for cat,cat_date in cats.items():
        c=add_cat(cat,cat_date)
        for p in cat_date["pages"]:
            add_page(c,p["title"],p["url"],p["views"])

    #打印添加的分类
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("{0}的{1}".format(str(c),str(p)))

def add_cat(name,cat_date):
    #c是一个分类对象
    c=Category.objects.get_or_create(name=name)[0]
    c.views=cat_date["views"]
    c.likes=cat_date["likes"]
    c.save()
    return c

def add_page(cat,title,url,views):
    p=Page.objects.get_or_create(category=cat,title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

if __name__ == "__main__":
    print("开始填充数据库")
    populate()