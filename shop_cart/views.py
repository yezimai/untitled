# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect,reverse
from shop_cart.models import UserShopCart
from django.http import JsonResponse
# Create your views here.

@login_required
@csrf_exempt
def cart(request):
    if request.method == "GET":
        cart_info = UserShopCart.objects.filter(user=request.user).all()
        return render(request,'shop_cart/cart.html',locals())
    else:
        #print(request.POST)
        id_list = request.POST.getlist('id')
        amount_list = request.POST.getlist('amount')
        new_list = zip(id_list,amount_list)
        # print 'amount_list-----',amount_list,id_list,new_list
        #print new_list
        # print 'new88888888888888_list',new_list,type(id_list),id_list,request.POST.get('csrfmiddlewaretoken')
        for i in new_list:
            # print i,i[0],type(i[0])
        #     obj=UserShopCart.objects.get(id=int(i[0]))
        #     #print obj
        #     obj.amount=int(i[1])
        #     obj.save()
        # #

            obj = UserShopCart.objects.filter(id=i[0])
            obj.update(amount=i[1])
        # print obj
        return redirect(reverse('shop_cart:order'))


@login_required
def order(request):

    order_list = UserShopCart.objects.filter(user=request.user)


    return render(request,'shop_cart/place_order.html',locals())

def update_cart(request):  #判断更新order
    return JsonResponse({'status':1})

def delete_cart(request,id):
    UserShopCart.objects.filter(id=id).delete()

    return JsonResponse({'status': 1})
