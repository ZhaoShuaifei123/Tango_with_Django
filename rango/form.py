from django import forms
from rango.models import Category,Page

#表单与表格不同，表单是让用户输入和选择的，要提交给服务器的
class CategoryForm(forms.ModelForm):
    #定义用ModelForm提供的什么小组件来装载字段,并且为组件命名，每次创建这个对象时候，都会根据属性创建一份下面定义的组件
    name=forms.CharField(max_length=128,help_text="请输入分类名称",label="名称")
    #widget=forms.HiddenInput()是隐藏小组件。另外，我们还设定了initial=0，把值设为零。这是把字段的默认值设为零的一种方式。
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes=forms.IntegerField(widget=forms.HiddenInput,initial=0)
    #required=False，制定这个字段的组件不是必须的
    slug=forms.CharField(widget=forms.HiddenInput(),required=False)

    #嵌套的类，为表单提供额外信息
    class Meta:
        #把上述的ModelForm与一个模型连接起来，切记切记切记要写，每次创建一个CategoryForm，就会创建一个包含Category各个字段的表单，
        model=Category
        #通过 fields 指定在表单中显示哪些字段（此处的就是可见字段）
        fields=('name',)


        #上述翻译到html界面是以下代码，隐藏的组件也创建了，只不过是隐藏的，仅仅显示meta类里面的。
        # < label for ="id_name" > Name:< / label > < input type = "text" name = "name" maxlength = "128" required  id = "id_name" >
        # < span class ="helptext" > 请输入分类名称 < / span > < input type="hidden" name="views" value="0" id="id_views" > < input type="hidden" name="likes" value="0" id="id_likes" > < input type="hidden" name="slug" id="id_slug" > < / p >




class PageForm(forms.ModelForm):
    #下面的小组件并不是必须要写的，一定要写上Meta类，并且关联上具体的模型类，表单上显示的都是fields上的，对于下面的小组件的定义会覆盖默认的小组件，不然就会使用默认的。
    title=forms.CharField(max_length=128,help_text="请输入页面标题名称",label='标题')
    url=forms.URLField(max_length=128,help_text="请输入页面的链接",label='链接')
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model=Page
        #通过 exclude 指定排除显示哪些字段，也可以用 fields=('title','url','views',)
        exclude=("category",)




