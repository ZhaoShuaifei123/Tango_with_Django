from django.template.defaultfilters import slugify
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128,unique=True)
    views=models.IntegerField(default=0)
    likes=models.IntegerField(default=0)
    #“i like django”,通过下面的SlugField()类型设置将slug设置成"i-like-django"
    slug=models.SlugField(unique=True)#url路径类型，并且添加唯一性约束

    #使用save（）时候，调用此函数
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
         self.slug=slugify(self.name)
         super(Category,self).save()

    #下面的方法可以让对象变成字符串表示形式。。此外， Django 会在管理后台中显示对象的字符串表示形式。
    def __str__(self):
        return self.name

    # 改变admin管理系统中表单的名称
    class Meta:
        verbose_name_plural = 'Categories'

class Page(models.Model):
    category=models.ForeignKey('Category',on_delete=models.CASCADE)#会在数据表中增加这个外键字段。值为外键的id
    title=models.CharField(max_length=128)
    url=models.URLField()
    views=models.IntegerField(default=0)

    def __str__(self):
        return self.title



