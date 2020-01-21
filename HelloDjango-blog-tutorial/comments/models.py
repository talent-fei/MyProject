from django.db import models
from django.utils import timezone

# Create your models here.

class Comment(models.Model):
    name = models.CharField('名字',max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址',blank=True)
    text = models.TextField('内容')
    create_time = models.DateTimeField('创建时间',default=timezone.now)
    # 所有的模型的字段都接受一个 verbose_name参数(大部分都是在第一个位置参数)
    # django在根据模型的定义自动生成表单时，会使用这个参数的值作为表单字段的label
    post = models.ForeignKey('blog.Post',verbose_name='文章',on_delete=models.CASCADE)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return '{}:{}'.format(self.name,self.text[:20])


