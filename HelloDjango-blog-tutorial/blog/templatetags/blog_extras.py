# 导入 template 这个模块，
from django import template
from ..models import Post,Categoty,Tag

# 实例化一个template.Library类
register = template.Library()

# 设置最新文档标签
# 将show_recent_posts装饰为register.inclusion_tag,告诉django 这个函数是我们自定义的一个类型为inclusion_tag的末班标签
@register.inclusion_tag('blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.all().order_by('-create_time')[:num],
    }

# 设置归档模板标签
@register.inclusion_tag('blog/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    return {
        'date_list':Post.objects.dates('create_time','month',order='DESC'),
    }

# 设置分类模板标签
@register.inclusion_tag('blog/inclusions/_categoties.html',takes_context=True)
def show_categoties(context):
    return {
        'categoty_list':Categoty.objects.all(),
    }

# 设置云模板标签
@register.inclusion_tag('blog/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    return {
        'tag_list':Tag.objects.all(),
    }