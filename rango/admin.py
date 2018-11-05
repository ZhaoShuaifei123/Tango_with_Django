from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
   #控制admin上slug表单数据会默认填充上name表单的内容
   prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
   # 控制admin上列表上显示的信息
   list_display = ("title","category","url")


#在Admin中注册上去模型
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)





