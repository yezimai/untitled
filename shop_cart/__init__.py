#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.signals import request_started
from django.dispatch import receiver
@receiver(request_started)
def fff(sender,**kwargs):
    pass
    #print('信号触发',sender)
    #print("\033[31;1m%s\033[0m"%kwargs)