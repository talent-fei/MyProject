# 导入django的form模块
from django import forms
from .models import Comment

# django的表单类必须继承自forms.ModelForm类或者forms.Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 表明这个表单对应的数据库模型是Comment类
        fields = ['name','email','url','text']  # 指明了表单需要显示的字段
