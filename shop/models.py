# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from tinymce.models import HTMLField

# Create your models here.


class GoodsCategory(models.Model):
    STATUS = (
        (0, u"正常"),
        (1, u"删除")
    )
    name = models.CharField(max_length=20, verbose_name=u"商品分类名")
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=u'状态')

    class Meta:
        verbose_name = u'商品分类'
        verbose_name_plural = verbose_name
        ordering = ('id',)
    def __unicode__(self):
        return '%s-%s'%(self.name,self.get_status_display())


class GoodsArea(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'商品产地')

    class Meta:
        verbose_name = u'商品产地'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __unicode__(self):
        return self.name


class GoodsInfo(models.Model):
    """
        商品类
    """
    STATUS = (
        (0, u"正常"),
        (1, u"删除")
    )

    name = models.CharField(max_length=30, verbose_name=u"商品名称")
    images = models.ImageField(
        upload_to='goods/%Y/%m/%d', verbose_name=u'商品图片地址')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=u'商品价格')
    click_count = models.IntegerField(default=0, verbose_name=u'商品点击量')
    unit = models.CharField(max_length=10, verbose_name=u'商品单位')
    status = models.IntegerField(choices=STATUS, default=0, verbose_name=u'状态')
    description = models.TextField(verbose_name=u'商品描述')
    stock = models.IntegerField(verbose_name=u'商品库存')
    detail = HTMLField()
    category = models.ForeignKey('GoodsCategory', verbose_name=u'商品分类')
    area = models.ForeignKey('GoodsArea', verbose_name=u'商品产地', null=True)

    class Meta:
        verbose_name = u'商品信息'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __unicode__(self):
        return '%s-%s'%(self.name,self.category_id)

from account.models import UserProfile
class UserRecord(models.Model):
    account = models.ForeignKey('account.UserProfile',null=True)  #注意这里的写法是夸APP调用model，写法是app名.表名
    goodsinfo = models.ForeignKey('GoodsInfo',null=True)
    access_time = models.DateTimeField(auto_now=True,null=True,blank=True) #注意这里的字段名是datetime不是date
                #auto_now就是获取用户的创建的时间，后面可以更改，不同于auto_now_add，他是字段的创建时间，后面不会改

    class Meta:
        unique_together=('account','goodsinfo')  #因为会生成多条1个用户访问一个商品的记录，所以创建一个联合唯一字段
        verbose_name='访问信息'
        verbose_name_plural = verbose_name
    def __unicode__(self): #这里是2.7的写法
        return '%s-%s-%s'%(self.account,self.goodsinfo_id,self.access_time)
