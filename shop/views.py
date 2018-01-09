# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.cache import cache_page
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import GoodsCategory,GoodsInfo,UserRecord
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.
from shop_cart.models import UserShopCart
def index(request):
	goods_list = []
	categorys = GoodsCategory.objects.filter(status=0).all()
	for c in categorys:
		goodsinfos = GoodsInfo.objects.filter(category=c).order_by('-id')[:4]
		goods_list.append({
			"goods_category":c,
			"goodsinfos":goodsinfos
		})
	return render(request, "shop/index.html",locals())
def get_filter_conditions(request):
	filter_conditions = {}
	for k,v in request.GET.items():
		if k in ['page']:
			continue
		if v:
			filter_conditions[k]=v
	# print '7777',filter_conditions
	return filter_conditions
def categorys(request,cid):
	"""
	cid就是category id
	使用分页查询商品
	"""
	# print '22222',request.GET.items()
	filter_conditions = get_filter_conditions(request)

	current_page = int(request.GET.get('page',1)) #获取页码
	curr_order = request.GET.get('curr_order','id')
	import collections
	order_map = collections.OrderedDict()
	order_map['id']=u'默认'
	order_map['price']=u'价格'
	order_map['click_count']=u'人气'

	# order_map = {
	# 	'id': '默认',
	# 	'price':'价格',
	# 	'click_count':'人气',
	# }
	current_goods_obj = GoodsInfo.objects.filter(category_id=cid).order_by(curr_order)
	if curr_order.startswith('-'):
		new_order_key = curr_order.strip('-')

	else:
		new_order_key = "-%s"%curr_order

	# print '----',current_goods_obj[0].name
	paginator = Paginator(current_goods_obj,10)  #默认显示5个
	try:
		querysets = paginator.page(current_page)
	except PageNotAnInteger:
		querysets = paginator.page(1)
	except EmptyPage:
		querysets = paginator.page(paginator.num_pages)
	return render(request,'shop/list.html',locals())

def detail(request,gid):
	goods_info = GoodsInfo.objects.get(pk=gid)
	# if request.user.is_authenticated():
	# 	from cache import BrowseCache
	# 	from django.db.models import F
	# 	browse = BrowseCache.get_browse(request.user)
	# 	if gid not in browse:
	# 		BrowseCache.set_browse(request.user,gid)
	# 		GoodsInfo.objects.filter(pk=gid).update(click_count=F('click_count')+1)

	if request.user.is_authenticated():
		record_obj=UserRecord.objects.filter(account=request.user,goodsinfo_id=gid) #在访问表中查找有没有该用户访问商品的记录
		count=record_obj.count()  #统计记录个数，如果有，则只更新访问时间
		from django.utils import timezone  #这里调用的是django 的timezone
		if count:
			record_obj[0].access_time=timezone.now()  #这里也要注意下前面models字段创建的写法是datetimefield
			record_obj[0].save()

		else:
			record_obj=UserRecord.objects.create(account_id=request.user.id,goodsinfo_id=gid)

			record_obj.save()
	return render(request,'shop/detail.html',locals())

@csrf_exempt
def shopping_list(request):
	if request.method == 'POST':
		print type(request.user)
		good_id = int(request.POST.get('select_good'))
		amount = int(request.POST.get('amount'))

		old_order_obj = UserShopCart.objects.filter(user=request.user).values('goodsinfo_id')
		# for obj in old_order_obj:
		# 	print '!!!!!!',obj.id
		#print 'old_order_id',old_order_obj,good_id
		# print ,type(good_id)
		# if good_id in old_order_obj:
		if  old_order_obj.filter(goodsinfo_id=good_id).count():  #判断这个商品是否在购物中，存在则将数量增加
			from django.db.models import F #不存在则新建一条购物单记录
			UserShopCart.objects.filter(user=request.user).update(amount=F('amount')+amount)
			return JsonResponse({'status':0})
		else:
			# print 'new order...'
			cart_obj = UserShopCart.objects.create(user=request.user, goodsinfo_id=good_id, amount=amount)
			cart_obj.save()
			return JsonResponse({'status':1})