from django.conf import settings

import xmpp
import time

def publish(sender, instance, created, **kwargs):
    """
    Publishes model to XMPP PubSub Node
    """
    print "publishing message %s %s" %(instance, created)

def create_node(node):
    """
    Creates a pubsub node on the xmpp server
    """
    print "creating pubsub node for %s" %node
