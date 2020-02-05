from django.db import models

# Create your models here.
class List(models.Model):
    pass

class Item(models.Model):
    # models.Model 的类映射到数据库中的一个表。
    # 默认情况下，这种类会得到一个自动生成的 id 属性，作为表的主键;
    text = models.TextField(default='')
    list = models.ForeignKey(List, default='')


