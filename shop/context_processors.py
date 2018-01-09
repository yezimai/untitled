# -*- coding:utf-8 -*-
from .models import GoodsCategory
from django.contrib.auth.decorators import login_required
from shop_cart.models import UserShopCart
def category_list(request):
	category_list = GoodsCategory.objects.filter(status=0).all()
	# print 'heheheheh', category_list
	return {"category_list": category_list}

def order_num(request):

    #if not request.user.username:
    if not request.user.is_authenticated():
        return {"order_nums":0}
    else:
        order_nums= UserShopCart.objects.filter(user=request.user).count()
        print 'order_num.....',order_nums
        return {"order_nums":order_nums}