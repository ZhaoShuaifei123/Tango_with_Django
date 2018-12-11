from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.urls import reverse
from registration.backends.simple.views import RegistrationView

from rango.models import Category,Page
from rango.form import  CategoryForm,PageForm
from rango.webhose_search import run_query


def get_server_side_cookie(request,cookie,default_val=None):
    #通过 requests.sessions.get() 检查 cookie 是否存在,因为request中有存放sessionid的cookie
    val=request.session.get(cookie)
    if not val:
        val=default_val
    return val

def visitor_cookie_handler(request):
    #获得或者创建一个cookie：visits,request.COOKIES.get这个方法获取的都会变成字符串类型
    visits=int(get_server_side_cookie(request,'visits','1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    #把last_visit变成Datetime类型
    last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    #设置成连续10s内访问不增加数值
    if(datetime.now()-last_visit_time).seconds>=10:
        visits=visits+1
        request.session['last_visit']=str(datetime.now())
    else:
        request.session['last_visit']=last_visit_cookie

    request.session['visits']=visits


def index(request):

    #想要赋值使用字典的话，必须要先定义字典
    context_dict = {}
    #查询数据库，获取前5个分类，放入上下文变量中
    category_list=Category.objects.order_by('-views')[:5]
    #创建上下文字典，渲染模板
    context_dict['category_list'] =category_list

    page_list=Page.objects.order_by('-views')[:5]
    context_dict['page_list']=page_list

    #调用处理 cookie 的辅助函数
    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']

    # render是生成一个response对象
    response = render(request, 'rango/index.html', context_dict)

    # 返回 response 对象，更新目标 cookie
    return response

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


@login_required
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

@login_required
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


#RangoRegistrationView类继承了RegistrationView，并且重写了get_success_url方法
class RangoRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('index')

def search(request):
    result_list=[]
    query_str=""
    if request.method == "POST":
        query_str=request.POST['query'].strip()
        if query_str:
            result_list=run_query(query_str)

    return render(request,"rango/search.html",{"result_list":result_list,"query_str":query_str})

@login_required
def like_category(request):
    cat_id = None
    print("怎么回事儿")

    if request.method == "GET":
        cat_id = request.GET['category_id']
    likes = 0
    if cat_id:
        cat =Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes+1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

def get_category_list(max_results=0,starts_with=""):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results>0:
        if len(cat_list)>max_results:
            cat_list=cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ""

    if request.method == "GET":
        starts_with = request.GET['suggestion']
    cat_list=get_category_list(8,starts_with)
    #render生成一个response对象，这个响应对象是经过数据渲染过的html代码。
    # 然后return返回给向这个函数发送请求的对象，可能是浏览器，可能是ajax请求
    return render(request,'rango/cats.html',{'cats':cat_list})























