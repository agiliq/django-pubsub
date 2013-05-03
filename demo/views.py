# Create your views here.

import time

from demo.forms import StatusForm
from demo.models import Status

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView


class MessageListView(ListView):

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context.update({
            'form': StatusForm(),
            'unique_nick': time.strftime("%s")
        })
        return context


class CreateStatusView(CreateView):
    model = Status
    success_url = '/pubsub'
