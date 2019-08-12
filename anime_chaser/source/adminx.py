import xadmin

from .models import Source


@xadmin.sites.register(Source)
class SourceAdmin:
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
