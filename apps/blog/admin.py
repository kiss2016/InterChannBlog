from django.contrib import admin

# Register your models here.

from .models import Article

#注册该模型
#admin.site.register(Article)
#@admin.register(Article)
class BlogAdmin(admin.ModelAdmin):
    #列表显示的字段
    list_display = ['article_id', 'title', 'publish_date']
    list_filter = ['article_id', 'title']
    list_display_links = ['title']
    class Media:
        js = (
            '/static/js/kindeditor/kindeditor-all.js',
            '/static/js/kindeditor/lang/zh_CN.js',
            '/static/js/kindeditor/config.js', #配置文件
        )
admin.site.register(Article, BlogAdmin)

admin.site.site_header = '后台管理系统'
admin.site.site_title = '接口渠道后台'