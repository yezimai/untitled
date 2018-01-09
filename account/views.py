# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View
from django.shortcuts import render,redirect,HttpResponse,reverse,HttpResponseRedirect
from .form import RegisterForm
from .models import UserProfile,EmailVerifyRecord,Receiver
from shop.models import UserRecord,GoodsInfo
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from utils.email import send_email
import json
# Create your views here.
def check_username(request):
    username = request.POST.get('username')
    count = UserProfile.objects.filter(username=username).count()
    return JsonResponse({"count":count})

class RegisterView(View):
    def get(self,request):
        return  render(request,'account/register.html',)
    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            response = self.save_user(request)
        return response
    def save_user(self,request):
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get('email')
        arrow = request.POST.get('allow')

        if arrow != '1':
            err_allow = u'请阅读我们的协议'
            return render(request,"account/register.html",locals())
        user=UserProfile()
        user.username=username
        user.email=email
        user.is_active=False
        user.password=make_password(password1)
        user.save()
        send_email(email,send_type=0)
        return redirect("/account/send_mail_success/")

def send_mail_success(request):

    return render(request,"account/send_success.html")

class ActiveView(View):
    def get(self,request,active_code):
        email_record = EmailVerifyRecord.objects.filter(code=active_code).first()
        if not email_record:
            err = {'message':u'注册码错误'}
            new_json = json.dumps(err,ensure_ascii=False)
            #return JsonResponse({'message':'注册码错误'.encode('utf-8')})
            return HttpResponse(new_json)
        else :
            user = UserProfile.objects.filter(email=email_record.email).first()
            user.is_active = True
            user.save()
            print('!!!!!',user.is_active)
            return redirect("/account/login")
def LoginView(request):
    if request.method== 'GET':
        return render(request, "account/login.html")
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:

            login(request,user)

            return redirect(request.GET.get('next') or '/shop/index')

            # from shop import views
            # return redirect(reverse(views.index))
        else:
            err = u"用户名或密码错误"
            return render(request, "account/login.html", locals())

class ModifyView(View):
    def get(self, request):
        return render(request, "account/forget_password.html")
    def post(self,request):
        email = request.POST.get('email')
        print('0000',email)
        user = UserProfile.objects.filter(email=email).count()
        if user:
            send_email(email, send_type=1)
            message = u"成功发送邮件"
        else:
            message = u"用户名不存在"
        print message
        return render(request, "account/forget_password.html", locals())

class ModifyPasswordView(View):
    def get(self,request,reset_code):
        email_record = EmailVerifyRecord.objects.filter(code=reset_code).first()
        if not email_record:
            return JsonResponse({"messge": u"错误"})
        else:
            email = email_record.email
            return render(request, "account/reset_password.html", locals())
    def post(self,request,reset_code):
        passwd1 = request.POST.get("password1")
        passwd2 = request.POST.get("password2")
        email = request.POST.get("email")

        if len(passwd1) < 8 and passwd1 != passwd2:
            err = u"密码设置错误"
            return render(request, "account/reset_password.html", locals())

        user = UserProfile.objects.filter(email=email).first()
        if not user:
            err = u"用户名不存在"
            return render(request, "account/reset_password.html", locals())
        else:
            # user.set_password = password1
            password = make_password(passwd1)
            user.password = password
            user.save()
            return redirect("/account/login/")

def logout_view(request):
    logout(request)
    return redirect("/shop/index")

@login_required
def user_center_info(request):
    # print('0000',request.user)
    # from shop.cache import BrowseCache
    # from shop.models import GoodsInfo
    # browse = BrowseCache.get_browse(request.user)
    # goods_info = GoodsInfo.objects.filter(id__in=browse) #上面是老师说的用cache做用户浏览统计的方法
    # print(request.user.id)
    goods_obj = UserRecord.objects.filter(account=request.user).values('goodsinfo')
    # print '===',goods_obj
    goods_info = GoodsInfo.objects.filter(id__in=goods_obj).order_by('-userrecord__access_time')  #注意这种写法，可以让goodinfo表按照record表的时间来排序
    #goods_info = GoodsInfo.objects.filter(id__in=goods_obj).order_by('-userrecord__id')
    # print '******',goods_info
    goods_info = list(goods_info)[0:5]
    record_nums = UserRecord.objects.filter(account=request.user).count()
    if record_nums>5:
        id=UserRecord.objects.filter(account=request.user).order_by('id')[0].id
        UserRecord.objects.filter(id=id).delete()
    return render(request, "account/user_center_info.html",locals())


@login_required
def user_center_site(request):
    if request.method == 'GET':
        receiver_infos = Receiver.objects.filter(user=request.user).all()
        # print(type(receiver_infos[0].id))
        return render(request, "account/user_center_site.html", locals())
    else:
        username = request.POST.get("username")
        city = request.POST.get("city")
        telephone = request.POST.get("telephone")
        address = request.POST.get("address")
        user_id = request.POST.get('user_id')
        # print('---------',user_id)
        if Receiver.objects.filter(id=user_id).count():
            receiver = Receiver.objects.get(id=user_id)
            receiver.user = request.user
            receiver.name = username
            receiver.address = address
            receiver.telephone = telephone
            receiver.city = city
            receiver.save()
        else:
            receive_obj=Receiver.objects.create(name=username,
                                    user=request.user,
                                    address = address,
                                    telephone=telephone,
                                    city=city
                                    )
            receive_obj.save()

        #return redirect("/account/user_center_site/")
        return redirect(reverse('user:user_center_site'))

@login_required
def user_center_set_default_site(request):
    data_id = request.GET.get("data_id")
    receiver = Receiver.objects.get(pk=data_id)
    request.user.receiver_name = receiver.name
    request.user.telephone_number = receiver.telephone
    request.user.city = receiver.city
    request.user.address = receiver.address
    request.user.receiver_id = receiver.id
    request.user.save()
    return JsonResponse({"telephone": receiver.telephone,
                         "address": receiver.address,
                         "name": receiver.name})

def user_center_del_default_site(request):
    data_id = request.GET.get("data_id")
    Receiver.objects.filter(id=data_id).delete()
    if request.user.receiver_id == int(data_id):
        request.user.receiver_name = None
        request.user.telephone_number = None
        request.user.city = None
        request.user.address = None
        request.user.receiver_id = 0
        request.user.save()
    return JsonResponse({"status": 0})

