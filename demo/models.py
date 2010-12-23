from django.db import models

# Create your models here.

from pubsub.utils import publish
from django.utils import simplejson

class Status(models.Model):
    """
    Status message of a user
    """
    message = models.CharField(max_length=140)
    nick = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time', )

    def save(self, *args, **kwargs):
        super(Status ,self).save(*args, **kwargs)

        payload = {}
        payload['message'] = self.message
        payload['nick'] = self.nick
        payload['time'] = str(self.time)

        payload_json = simplejson.dumps(payload)
        print payload_json
        publish("/demo/Status", payload_json)
