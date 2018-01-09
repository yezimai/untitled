# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserShopCart(models.Model):
    user = models.ForeignKey('account.UserProfile',null=True)
    goodsinfo = models.ForeignKey('shop.GoodsInfo',null=True)
    amount = models.IntegerField(default=1)
    class Meta:
        verbose_name=u'用户购物车'
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return '%s-%s-%s'%(self.user,self.goodsinfo,self.amount)
