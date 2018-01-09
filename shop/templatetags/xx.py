# -*- coding:utf-8 -*-
from django.template import Library
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

register = Library()
@register.simple_tag
def divide_page(current_page,paginator,conditions): #current_page是当前页的页码，int(request.GET.get('page',1))
                                    # paginator是一个页码的对象，paginator = Paginator(current_goods_obj,3)#默认显示5个
    max_page_count=5 #显示的最大页码
    page_str = ''  #要返回前端显示的页面
    print '---->tag,coditions',conditions
    mid_page = max_page_count/2  #中间页码
    page_range = [c for c in paginator.page_range]  #生成所有页码的列表
    # print page_range
    page_index = page_range.index(current_page)  #找到当前页码的索引
    if page_index > mid_page:  #当前页码大于我们设定的中间页码时
        curr_page_range = page_range[page_index-mid_page:]  #将页码集合中小于索引减去中间页码的值取出来，生成新的列表
        if len(curr_page_range) < 5:    #如果当前列表的元素没有5个了，那么我就把最后5个元素取出来当成新的列表
           curr_page_range = page_range[-5:]
    else:   #如果当前页码小于我们的中间页码时，我们就取默认的所有页码的列表
        curr_page_range = page_range
    i=1  #计数器，规定只取5个页码出来

    for cp in curr_page_range:  #循环这个页码列表，如果页码等于我们当前页的页码，就把他的增加样式，否则正常显示
        if cp == current_page:
            page_str += '<a href="?page=%s%s" class="active" style="background-color: #1b6d85">%s</a>'%(cp,conditions,cp)
        else:
            page_str += '<a href="?page=%s%s" >%s</a>'%(cp,conditions,cp)
        i+=1
        if i>max_page_count:    #计算器大于5结束循环
            break
    return mark_safe(page_str)
@register.simple_tag
def condtions_html(filter_conditions):
    conditions = ''
    for k,v in filter_conditions.items():
        if v:
            conditions += "&%s=%s"%(k,v)
    return conditions


@register.simple_tag
def order_tag(order_map,curr_order,new_order_key):
    html_ele=''
    if new_order_key.startswith('-'):
        #icon_ele = '<i class="glyphicon glyphicon-menu-down" aria-hidden="true"></i>'
        icon_ele = '<i class="fa fa-angle-down"></i>'
    else:
        # icon_ele = '<i class="glyphicon glyphicon-menu-up" aria-hidden="true"></i>'
        icon_ele = '<i class="fa fa-angle-up"></i>'
    for k,v in order_map.items():
        if k in curr_order:
            html_ele += '<a href="?curr_order=%s" class="active" >%s%s</a>'%(new_order_key,v,icon_ele)

        else:
            html_ele += '<a href="?curr_order=%s">%s</a>' %(k, v)
    return mark_safe(html_ele)

@register.inclusion_tag("shop/refferral_good.html")
def refferral_goods(cid=None):
    from shop.models import GoodsInfo
    from django.conf import settings
    if cid:
        refferral_goods=GoodsInfo.objects.filter(category_id=cid).order_by('-id')[:2]
    else:
        refferral_goods = GoodsInfo.objects.all().order_by('-id')[:2]
    return {
        "refferral_goods":refferral_goods,
        "MEDIA_URL":settings.MEDIA_URL
    }

@register.simple_tag
def get_category_name(cid):
    from shop.models import GoodsCategory
    category_name = GoodsCategory.objects.get(id=cid).name
    return category_name
@register.simple_tag
def default_address(user_obj):
    #print 'oooooo',type(user_obj.receiver_set),user_obj.receiver_set
    from account.models import Receiver
    receiver_obj=Receiver.objects.filter(id=user_obj.receiver_id,user=user_obj)[0]
    html_ele='%s-%s-%s-%s'%(
        receiver_obj.name,
        receiver_obj.city,
        receiver_obj.address,
        receiver_obj.telephone,
    )
    return html_ele
@register.simple_tag
def get_filter_conditions(request):
	filter_conditions = {}
	for k,v in request.GET.items():
		if k in ['page']:
			continue
		if v:
			filter_conditions[k]=v
	# print '7777',filter_conditions
	return filter_conditions

@register.simple_tag
def get_q_keyname(request):
    #print('6666',request.GET.items)
    for k,v in request.GET.items():
        if k in ['q']:
            q_val = v

            print '!!!',q_val #苹果
            return q_val
        else:
            return ''