import sys
_self = sys.modules[__name__]
get = lambda v, default=None: getattr(_self, v, default)

MAC_ADDR = '0a:00:00:00:00:00'
DEBUG = True
USERNAME = 'qweeze'
