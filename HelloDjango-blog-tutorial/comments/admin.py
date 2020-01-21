from django.contrib import admin
from .models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','url','post','create_time']
    fields = ['name','email','url','text','post']

#注册的comments名称空间
admin.site.register(Comment,CommentAdmin)
