from django.shortcuts import render
from django.http import HttpResponse
import re
import markdown
from django.utils.text import slugify
from django.shortcuts import render,get_object_or_404
from markdown.extensions.toc import TocExtension

from .models import Post,Categoty,Tag

# Create your views here.

# 定义主页视图
def index(request): # request就是django为我们封装好的HTTP请求，他是类HttpResponse的一个实例
    # 返回HTTP响应给用户，也就是django给我们封装好的
    # return HttpResponse("欢迎访问我的博客首页")

    # return render(request,'blog/index.html',context={
    #     'title':'我的博客首页',
    #     'welcome':'欢迎访问我的博客首页'
    # })

    # 因为在models中Post的Meta中，我们定义了文章排序的方式，因此，这边就不用设置order_by了
    post_list = Post.objects.all()

    # post_list = Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',context={
        'title':'博客首页',
        'post_list':post_list
    })

# 定义详情页视图
def detail(request,pk):
    post = get_object_or_404(Post,pk = pk)
    md = markdown.Markdown(extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',  # 设置diaman代码语法高亮拓展
            # 'markdown.extensions.toc',  # 设置允许自动生成目录
            # 使用TocExtension的实例，其slugify参数可以接受一个函数，这个函数可以被用来处理标题的锚点值
            # Markdown 内置的处理方法不能直接处理中文标题，所以我们可以使用django.utils.text中的slugify方法
            TocExtension(slugify = slugify), # 取消不再使用字符串markdown.extensions.toc
            ])
    post.body = md.convert(post.body)
    # 分析toc内容，如果有目录结构，ul标签中就有值，通过正则检测
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    # 得到post.toc内容
    post.toc = m.group(1) if m is not None else ''
    print(post.toc)

    return render(request,'blog/detail.html',context={'post':post})

# 定义归档视图函数
def archive(request,year,month):
    # 使用filter来根据条件过滤
    post_list = Post.objects.filter(
        create_time__year=year,
        create_time__month = month)
    return render(request,'blog/index.html',context={'post_list':post_list})

# 定义分类视图函数
def categoty(request,pk):
    # 记得在开始部分导入Categoty
    cate = get_object_or_404(Categoty,pk = pk)
    post_list = Post.objects.filter(categoty = cate)
    return render(request,'blog/index.html',context={'post_list':post_list})

# 定义标签云视图函数
def tag(request,pk):
    t = get_object_or_404(Tag,pk = pk)
    post_list = Post.objects.filter(tags = t)
    return render(request,'blog/index.html',context={'post_list':post_list})



