from django import template
from rango.models import Category

register=template.Library()

#下面是装饰器，函数 get_category_list() 需要模板cats.html的支持
#自定义了参数化模板标签
@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats':Category.objects.order_by('-views')[:8],
            'act_cat':cat}

