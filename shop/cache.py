# -*- coding:utf-8 -*-
from django_redis import get_redis_connection

conn =get_redis_connection("default")

class BrowseCache(object):
    user_browse_cache_key = "user_browse_cache_key_{0}"

    @classmethod
    def set_browse(cls,user,gid,default=0):
        conn.zadd(cls.user_browse_cache_key.format(user.id),str(1),gid)
    @classmethod
    def get_browse(cls,user,start=-5,end=-1):
        record=conn.zrange(cls.user_browse_cache_key.format(user.id),start,end)
        print record
        return record