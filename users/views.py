from django.shortcuts import render
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
