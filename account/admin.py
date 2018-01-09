# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import EmailVerifyRecord,UserProfile,Receiver
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(EmailVerifyRecord)
admin.site.register(UserProfile)
admin.site.register(Receiver)
