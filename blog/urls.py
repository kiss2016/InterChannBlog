from django.urls import path, include
import blog.views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    # path('content', blog.views.article_content),
    path('index', blog.views.get_index_page),
    # path('detail', blog.views.get_detail_page),
    path('detail/<int:article_id>', blog.views.get_detail_page),
    path('protocol/standardetail/<int:article_id>', blog.views.get_standardetail_page),
    path('iboss', blog.views.get_iboss_page),
    path('protocol', blog.views.get_protocol_page),
    path('channel', blog.views.get_channel_page),
    path('interface', blog.views.get_interface_page),
    path('other', blog.views.get_other_page),
    path('search', blog.views.search, name='search'),
    # url(r'^static/(?P<path>.*)$', serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = blog.views.PageNotFound