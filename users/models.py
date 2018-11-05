from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    #这一行是必须的,建立与 User 模型之间的关系,User模型是Django自带的，我们为User模型添加自己个性化的属性
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    #添加自己的属性，自己网站的链接和头像
    website=models.URLField(blank=True)
    #注意ImageField字段的upload_to参数。这个参数的值与项目的MEDIA_ROOT设置结合在一起，确定上传的头像存储在哪里。假如MEDIA_ROOT的值为< workspace > / tango_with_django_project / media /，
    # upload_to参数的值为profile_images，那么头像将存储在 < workspace > / tango_with_django_project / media / profile_images / 目录中
    picture=models.ImageField(upload_to="profile_images",blank=True)


    def __str__(self):
        return self.user.username
