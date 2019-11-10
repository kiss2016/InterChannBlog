import xadmin
from xadmin import views
# Register your models here.
from xadmin.views import BaseAdminView
from xadmin.views import CommAdminView
from .models import Article

# @xadmin.register(Article)
class BlogAdmin(object):
    list_display = ['article_id', 'title', 'publish_date']
    list_filter = ['article_id', 'title']
    list_display_links = ['title']

# 注册该模型
xadmin.site.register(Article, BlogAdmin)


#配置主题设置
class ThemeAdmin(object):
    enable_themes=True
    use_bootswatch=True
xadmin.site.register(BaseAdminView,ThemeAdmin)

#网页头部导航标题 底部信息
class CustomAdmin(object):
    site_title='后台管理系统'
    site_footer='接口渠道专用'
    #设置伸缩
    menu_style='accordion'
xadmin.site.register(CommAdminView,CustomAdmin)