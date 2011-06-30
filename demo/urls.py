from django.conf import settings
from django.conf.urls.defaults import *

from demo.models import Status
from demo.forms import StatusForm
import time

urlpatterns = patterns('',
    url(r'^status/new$', 'django.views.generic.create_update.create_object', {
        'model': Status,
        'post_save_redirect': '/pubsub',
        }, name='pubsub_status_new'),
    url(r'^$', 'django.views.generic.list_detail.object_list', {
        'queryset': Status.objects.all()[getattr(settings, 'MAX_STATUSES_NUM', 50)],
        'extra_context': {'form': StatusForm(),
            'unique_nick': time.strftime("%s")}
        }),
)
