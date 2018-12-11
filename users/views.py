from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from users.form import UserForm,UserProfileForm
# Create your views here.

def register(request):
    registed=False

    #提交过来的表单，则需要存储到数据库
    if request.method == "POST":
        #创建表单对象，并给表单赋值
        userform=UserForm(data=request.POST)
        userprofileform=UserProfileForm(data=request.POST)
        if userform.is_valid()and userprofileform.is_valid():
            #表单对象的sava方法，会生成一个相应的数据库表对象
            user=userform.save(commit=False)
            # 使用 set_password 方法计算密码哈希值
            # 然后更新 user 对象
            user.set_password(user.password)
            user.save()

            userprofile=userprofileform.save(commit=False)
            userprofile.user=user

            # 用户提供头像了吗？如果用户上传了头像，还要处理头像图片
            # 如果提供了，从表单数据库中提取出来，赋给 UserProfile 模型
            if 'picture' in request.FILES:
                userprofile.picture = request.FILES['picture']

            userprofile.save()
            registed=True
        else:
            # 表单数据无效，出错了？
            # 在终端打印问题
            print(userform.errors, userprofileform.errors)

    #首次访问，则需要返回给用户空界面
    else:
        userform = UserForm()
        userprofileform = UserProfileForm()

    context={"userform":userform,"userprofileform":userprofileform,"registed":registed}

    return render(request,"users/register.html",context)

def user_login(request):

    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        # 使用 Django 提供的函数检查 username/password 是否有效,
        # 如果有效，返回一个 User 对象,如果失败则会返回None对象
        user=authenticate(username=username,password=password)

        # 如果得到了 User 对象，说明用户输入的凭据是对的
        # 如果是 None（Python 表示没有值的方式），说明没找到与凭据匹配的用户
        if user:
            # 账户激活了吗？可能被禁了
            if user.is_active:
                # 登入有效且已激活的账户
                login(request,user)

                #重定向到首页
                #使用Django提供的reverse()函数获取Rango应用首页的URL。
                # reverse()函数在Rango应用的urls.py模块中查找名为index的URL模式，解析出对应的URL
                #return HttpResponseRedirect(reverse('index'))
                return redirect(reverse('index'))
            else:
                #视图返回一个 HttpResponse 对象。简单的 HttpResponse 对象的参数是一个字符串，表示要发给客户端的页面内容。
                return HttpResponse('账号被封禁了......')

        else:
            print("无效的账号{0},密码{1}".format(username,password))
            print("无效的账号：%s,密码：%s"%(username,password))
            return HttpResponse("无效的账号，密码")

    # 不是 HTTP POST 请求，显示登录表单
    # 极有可能是 HTTP GET 请求
    else:
        # 没什么上下文变量要传给模板系统
        # 因此传入一个空字典
        return render(request,'users/login.html',{})

@login_required
def user_logout(request):

    logout(request)
    return redirect(reverse('index'))




