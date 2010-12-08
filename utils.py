from django.conf import settings

import xmpp
import time

def publish(sender, **kwargs):
    """
    Publishes model to XMPP PubSub Node
    """
    jid = xmpp.protocol.JID(settings.JABBER_ID)
    client = xmpp.Client(jid.getDomain(), debug=[])
    conn = client.connect()
    if conn:
        auth = client.auth(jid.getNode(), settings.JABBER_PASSWORD, resource=jid.getResource())
        if auth:
            id = client.send(xmpp.protocol.Message(settings.JABBER_RECIPIENT, settings.JABBER_ERROR_TEXT))
            time.sleep(1)

def create_node(node):
    """
    Creates a pubsub node on the xmpp server
    """
    print "creating pubsub node for %s" %node
