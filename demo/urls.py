from django.conf import settings
from django.conf.urls.defaults import *

from demo.models import Status
from demo.views import MessageListView, CreateStatusView


urlpatterns = patterns('',
    url(r'^status/new$', CreateStatusView.as_view(),  name='pubsub_status_new'),
    url(r'^$', MessageListView.as_view(
                queryset=Status.objects.all()[:getattr(settings, 'MAX_STATUSES_NUM', 50)],
            ),
        )
)
