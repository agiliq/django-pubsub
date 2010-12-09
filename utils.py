from django.core import serializers
from django.conf import settings

import xmpp
import time

def publish(sender, instance, created, **kwargs):
    """
    Publishes model to XMPP PubSub Node
    """
    #print "publishing message %s %s %s" %(instance, created, make_node(sender))
    pub_iq = xmpp.protocol.Iq(typ='set',
                           to=getattr(settings, 'XMPP_PUBSUB_HOST'),
                           attrs={'id': str(instance.id)})
    pub_iq.T.pubsub = ""
    pub_iq.T.pubsub.namespace = xmpp.protocol.NS_PUBSUB
    pub_iq.T.pubsub.T.publish = ""
    pub_iq.T.pubsub.T.publish['node'] = make_node(sender)
    pub_iq.T.pubsub.T.publish.T.item = ""
    pub_iq.T.pubsub.T.publish.T.item.T.entry = ""
    pub_iq.T.pubsub.T.publish.T.item.T.entry.namespace = 'http://www.w3.org/2005/Atom'
    instance_xml = serializers.serialize('xml', [instance, ])
    instance_node = xmpp.simplexml.NodeBuilder(instance_xml).getDom()
    pub_iq.T.pubsub.T.publish.T.item.T.entry.addChild(node=instance_node)
    print pub_iq


def make_node(model):
    """
    Makes a pubsub node from a model

    E.g. node for 'blog.models.Entry'
    would be '/blog/models/Entry'
    """
    return "/%s/%s" %(model.__module__.replace('.', '/'),
            model.__name__)

