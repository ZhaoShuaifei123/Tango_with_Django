from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from rango.models import Category,Page
from rango.form import  CategoryForm,PageForm

def index(request):
    #想要赋值使用字典的话，必须要先定义字典
    context_dict = {}
    #查询数据库，获取前5个分类，放入上下文变量中
    category_list=Category.objects.order_by('-likes')[:5]
    #创建上下文字典，渲染模板
    context_dict['category_list'] =category_list
    #渲染响应，发给客户端

    page_list=Page.objects.order_by('-views')[:5]
    context_dict['page_list']=page_list

    return render(request,'rango/index.html',context_dict)

def show_category(request,category_name_slug):
    context_dict={}
    category = Category.objects.get(slug=category_name_slug)
    context_dict["category"]=category
    try:
        pages=Page.objects.filter(category=category)
        context_dict["pages"]=pages
    except "page.doesnotexist":
        context_dict['pages']=None

    return render(request,'rango/category.html',context_dict)

def about(request):
    #html代码可以直接返回给浏览器，浏览器会进行解析。所以可以在python中写html代码，python把它当字符串处理，返回给浏览器后，浏览器会进行解析。
    # return HttpResponse("<hr>"+"<h2>关于</h2>"+"<hr>")
    return render(request,'rango/about.html',{})

def add_category(request):
    #创建一个CategoryForm对象
    form = CategoryForm()
    #HTTP GET请求 获取指定资源的表述。即HTTP GET请求用于获取特定的资源,例如一个网页、一张图像或一个文件。
    #HTTP POST请求 向服务器中提交数据，一般还会存入数据库。
    #判断是不是HTTP POST请求，即是不是提交数据过来的，如果不是的话，则是首次访问页面过来添加数据的
    if request.method == "POST":
        #把数据放到CategoryForm中，生成一个新CategoryForm对象，名字还是form
        form=CategoryForm(request.POST)

        #表单数据有效吗？
        if form.is_valid():
            #调用save函数，会生成一个Category对象，并且将表单数据存到对象里，commit=True会把新分类对象存入数据库
            cat=form.save(commit=True)#通过表单创建一个对象
            #调用index（）函数，必须要有请求对象作为参数，把用户带到首页
            print(cat)
            return index(request)

        else:
            #表单数据有错误,在服务器的终端（控制台）里打印出来
            print(form.errors)
            return render(request, 'rango/add_category.html', {"form": form})

    return render(request,'rango/add_category.html',{"form":form})

def add_page(request,category_name_slug):

    try:
        category=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None

    form=PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            ##Pageform调用save函数，会生成一个Page对象，并且将表单数据存到对象里，commit=False不会把表单数据存入数据库
            page=form.save(commit=False)
            page.category=category
            page.views=0
            page.save()
            return show_category(request,category_name_slug)
        else:
            print(form.errors)
            #context_dict = {"form": form, "category": category}
            #return render(request,"rango/add_page.html",context_dict)

    context_dict={"form":form,"category":category}
    return render(request,"rango/add_page.html",context_dict)











