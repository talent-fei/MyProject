from django import template
from ..forms import CommentForm

register = template.Library()

# 评论表单视图函数
@register.inclusion_tag('comments/inclusions/_form.html',takes_context=True)
def show_comment_form(context,post,form=None):
    if form is None:
        # 如果没有接收到评论表单的参数，模板标签就会新创建一个CommentForm的实例
        # 即一个没有绑定过任何数据的空表单 传给模板，否则就直接将接收到的评论表单实例传递给模板
        # 达到复用已有的评论表单实例
        form = CommentForm()
    return {
        'form':form,
        'post':post,
    }

# 评论内容视图函数
@register.inclusion_tag('comments/inclusions/_list.html',takes_context=True)
def show_comments(context,post):
    comment_list = post.comment_set.all()
    comment_count =comment_list.count()
    return {
        'comment_list':comment_list,
        'comment_count':comment_count,
    }