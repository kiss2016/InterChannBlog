from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class BlogConfig(AppConfig):
    name = 'blog'
    #app名字后台显示中文
    verbose_name = u"资料库"


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'