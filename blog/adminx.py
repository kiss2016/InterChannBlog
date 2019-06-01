import xadmin
from xadmin import views
# Register your models here.

from .models import Article

# @xadmin.register(Article)
class BlogAdmin(Article):
    list_display = ['title', 'publish_date']

# 注册该模型
xadmin.site.register(Article)