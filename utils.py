from django.conf import settings

import xmpp
import time

def publish(sender, instance, created, **kwargs):
    """
    Publishes model to XMPP PubSub Node
    """
    print "publishing message %s %s %s" %(instance, created, make_node(sender))

def make_node(model):
    """
    Makes a pubsub node from a model

    E.g. node for 'blog.models.Entry'
    would be '/blog/models/Entry'
    """
    return "/%s/%s" %(model.__module__.replace('.', '/'),
            model.__name__)

