from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


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
        ('other', u'其他')
    )
    lable = models.CharField('模块', max_length=6, choices=labels, default=None, blank=False)
    # 文章的摘要
    brief_content = models.TextField('摘要', blank=True)
    # 文章的主要内容
    content = RichTextUploadingField('内容', blank=False)
    # 文章的发布日期
    publish_date = models.DateTimeField('发布日期', auto_now=True)

    def __str__(self):
        return self.title
