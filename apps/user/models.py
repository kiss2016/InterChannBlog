from django.db import models
from django.contrib.auth.models import AbstractUser # 用户验证类
from base_models.base_model import BaseModel

# Create your models here.
class User(AbstractUser, BaseModel):
    """用户模型类"""

    class Meta:
        db_table = 'subscriber'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
