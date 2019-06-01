from django.contrib import admin

# Register your models here.

from .models import Article

#注册该模型
#admin.site.register(Article)
#@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    #列表显示的字段
    list_display = ['title', 'publish_date']
class Media:
    js = (
        '/static/js/kindeditor/kindeditor-min.js',
        '/static/js/kindeditor/lang/zh_CN.js',
        '/static/js/kindeditor/config.js', # 配置文件，这个需要自己实现
    )
admin.site.register(Article, BlogAdmin)