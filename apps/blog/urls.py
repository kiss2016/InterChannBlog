from django.urls import path, include
from apps.blog import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import routers, serializers, viewsets

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'ckeditor/', include('ckeditor_uploader.urls')),
    # path('content', blog.views.article_content),
    path('index', views.get_index_page,name='index'),
    path('', views.get_index_page,name='index'),
    # path('detail', views.get_detail_page),
    path('detail/<int:article_id>', views.get_detail_page),
    path('protocol/standardetail/<int:article_id>', views.get_standardetail_page),
    path('iboss', views.get_iboss_page),
    path('protocol', views.get_protocol_page),
    path('channel', views.get_channel_page),
    path('interface', views.get_interface_page),
    path('other', views.get_other_page),
    path('search', views.search, name='search'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    url(r'^bardata/$', views.bardata),
    url(r'^piedata/$', views.piedata),
    url(r'^ibossauto/$', views.IndexView.as_view(), name='blog'),
    url(r'^ibossauto/CQiboss/$', views.CQView.as_view(), name='blog'),
    url(r'^ibossauto/SDiboss/$', views.SDView.as_view(), name='blog'),
    url(r'^ibossauto/HUBiboss/$', views.HUBView.as_view(), name='blog'),
    url(r'^ibossauto/HEBiboss/$', views.HEBView.as_view(), name='blog'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.PageNotFound