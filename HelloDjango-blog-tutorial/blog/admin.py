from django.contrib import admin

# Register your models here.
from .models import Post,Categoty,Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','modified_time','categoty','author']
    fields = ['title','body','excerpt','categoty','tags']

    def save_model(self,request,obj,form,change):
        obj.author = request.user
        super().save_model(request,obj,form,change)

# 把新增的 PostAdmin 也注册进来
admin.site.register(Post,PostAdmin)
admin.site.register(Categoty)
admin.site.register(Tag)
