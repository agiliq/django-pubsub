from django.core import serializers
from django.conf import settings

import xmpp
import time

class XMPPException(Exception):
    pass

def handle_post_save(sender, instance, created, **kwargs):
    """
    handles the post_save signal of registered models
    to publish messages
    """
    pub_iq = build_iq(make_node(sender), "")
    instance_xml = serializers.serialize('xml', [instance, ])
    instance_node = xmpp.simplexml.NodeBuilder(instance_xml).getDom()
    pub_iq.T.pubsub.T.publish.T.item.T.entry.addChild(node=instance_node)
    send_message(pub_iq)

def publish(node, payload):
    """
    Publishes model to XMPP PubSub Node
    """
    iq = build_iq(node, payload)
    send_message(iq)

def build_iq(node, payload):
    iq = xmpp.protocol.Iq(typ='set',
            to=getattr(settings, 'XMPP_PUBSUB_HOST'))
    iq.T.pubsub = ""
    iq.T.pubsub.namespace = xmpp.protocol.NS_PUBSUB
    iq.T.pubsub.T.publish = ""
    iq.T.pubsub.T.publish['node'] = node
    iq.T.pubsub.T.publish.T.item = ""
    iq.T.pubsub.T.publish.T.item.T.entry = payload
    iq.T.pubsub.T.publish.T.item.T.entry.namespace = 'http://www.w3.org/2005/Atom'
    return iq

def send_message(msg):
    """
    Sends a IM `msg` using xmpppy

    msg should be a xmpp.protocol.Message instance
    """
    from_jid = xmpp.protocol.JID(getattr(settings, 'XMPP_JID'))
    passwd = getattr(settings, 'XMPP_PASSWORD')

    print msg
    client = xmpp.Client(from_jid.getDomain(), debug=[])
    if client.connect():
        if client.auth(from_jid.getNode(), passwd):
            client.send(msg)
            time.sleep(1)
        client.disconnect()

def make_node(model):
    """
    Makes a pubsub node from a model

    E.g. node for 'blog.models.Post'
    would be '/blog/Post'
    """
    return "/%s/%s" %(model.__module__.split(".")[0],
            model.__name__)

