# Create your models here.
import markdown
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.models import User

class Categoty(models.Model):
    '''
    django 要求模型必须继承models.Model类
    Categoty 只需要一个简单的分类名 name 就可以了
    CharField 指定了分类名的 name 的数据类型，CharField是字符型
    CharFiled 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能存入数据库
    当然，django还为我们提供了多种其他的数据类型，比如日期时间类型DateTimeField、整数类型IntegerField等等
    django内置的全部分类可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    '''

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class Tag(models.Model):
    '''
    标签 Tag 也比较简单，和 Categoty一样。
    再次强调一次继承 models.Model类
    '''

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)

class Post(models.Model):
    '''
    文章的数据库表稍微负载一点，主要涉及的字段比较多
    '''

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # ordering属性用来指定文章的排序方式
        ordering = ['-create_time']

    def __str__(self):
        return self.title

    # 为了方便地生成url，定义get_absolute_url方法
    # 自定义get_absolute_url方法
    # 记得从 django.urls 中导入 resversed 函数
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    # 文章的标题
    title = models.CharField('标题',max_length=70)

    # 文章正文，我们使用了TextField
    # 存储比较短的字符串的时候可以使用CharField，但是对于文章的正文可能会是一大段文本，因此使用TextField来存储大端文本
    body = models.TextField('正文')

    # 这两个分别表示文章的创建时间和最后一次修改时间，存储时间的字段用DateTimeField
    create_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要，可以没有文章摘要，但默认情况下CharField要求我摩恩必须存入数据，否则就会报错
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了
    excerpt = models.CharField('摘要',max_length=200,blank=True)

    # 这是分类与标签，分类与标签的模式我们已经定义在上面
    # 我们在这里把文章对应的数据库和分类，标签对应的数据库表关联起来，但是关联形式稍微有点不同
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是ForeignKey，即一对多
    # 的关联关系，且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定关联的数据被删除时，
    # 被关联的数据的行为，我们这里假定：当某个分类被删除时，该分类下全部文章也同时被删除，因此，使用
    # models.CASCADE 参数，意味级联删除
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用ManyToManyField，表明这是
    # 多对多的关联关系
    # 同时我们规定文章可以没有标签，因此标签tags指定了blank = True
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    categoty = models.ForeignKey(Categoty,verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,verbose_name='标签',blank = True)

    # 文章作者，这里 User 是从django.contrib.auth.models 导入的
    # django.contrib.auth 是 django 的内置应用，专门用于处理网站用户的注册、登录等流程， User是 django为我们写好的
    # 用户模型，这里我们通过 ForeignKey 把文章和 User 关联起来
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一个一对多的关系，和Category相似
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    # 设置文章第二次修改时间
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个Markdown类，用于渲染body的文本
        # 由于摘要并不需要生成文章目录，所以去掉目录扩展
        md = markdown.Markdown(extension=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前54个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)


