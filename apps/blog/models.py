from django.db import models
from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


# Create your models here.
class Article(models.Model):
    # 文章的唯一ID
    article_id = models.AutoField('编号', primary_key=True)
    # 文章标题
    title = models.CharField('标题', max_length=32)
    # 文章所属模块
    labels = (
        ('iboss', u'一级boss'),
        ('channel', u'渠道'),
        ('interface', u'短厅'),
        ('other', u'其他'),
        ('tocol', u'协议'),
    )
    lable = models.CharField('模块', max_length=32, choices=labels, default=None, blank=False)
    # 文章的摘要
    brief_content = models.TextField('摘要', blank=True)
    # 文章的主要内容
    # content = RichTextField('内容', blank=False)
    content = RichTextField(blank=True, null=True, verbose_name="内容")
    # content = RichTextUploadingField('内容',blank=False)
    # 文章的发布日期
    publish_date = models.DateTimeField('发布日期', auto_now=True)
    # 定义文章作者。 author 通过 models.ForeignKey 外键与内建的 User 模型关联在一
    # 参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。通常设置为 CASCADE 级联删除就可以了
    author = models.OneToOneField("user.User", on_delete=models.CASCADE, to_field='username', default='admin',
                                  verbose_name='作者')
    # 浏览量
    total_views = models.PositiveIntegerField('浏览量', default=0)
    # 文章点赞数
    likes = models.PositiveIntegerField('点赞数', default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
