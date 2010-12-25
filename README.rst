Overview:
=========

django-pubsub allows you to create Twitter like real-time updates for your models.

PubSub is a way to publish and subscribe to events over XMPP. Instead of intensive polling,
it relies on the publisher pushing the information and the client subscribing and receiving the
events.

django-pubsub makes use of the XMPP pubsub implementation (refer to `XEP 0060 <http://xmpp.org/extensions/xep-0060.html>`_ for details).

You will need:

1. An XMPP server with pubsub support (tested with ejabberd)
2. A BOSH transport to XMPP (tested with nginx and ejabberd)
3. xmpppy
4. Strophe.js and pubsub plugin

Usage:
======

Publish:
--------

You have "Tweet" model in your models and you want to make the updates
real-time.

Just do::

    from pubsub import pubsub

    pubsub.register(Tweet)

You can register multiple models by passing them in a list. Each registered
model becomes a ``Publisher`` ``Node`` and will notify all subscribers about any new
instances created. The ``node`` created is named after the app and the model. If your app is named
Twitter, your node for ``Tweet`` model would be ``/Twitter/Tweet``. The payload passed along
with the notification includes the instance serialized to XML.

You can also publish events to nodes anywhere in your view with::

    from pubsub import publish
    publish("/home", "Hello World")

Subscribe:
----------

A XMPP client written in strophe.js will listen to the ``Publisher`` and
receive events. The app includes a client in ``media/js``.

To use the client you need to include::

    <script type="text/javascript" src="{{ MEDIA_URL }}/js/jquery-1.4.2.min.js"></script>
    <script type="text/javascript" src="{{ MEDIA_URL }}/js/strophe.js"></script>
    <script type="text/javascript" src="{{ MEDIA_URL }}/js/strophe.pubsub.js"></script>
    <script type="text/javascript" src="{{ MEDIA_URL }}/js/pubsub.settings.js"></script>
    <script type="text/javascript" src="{{ MEDIA_URL }}/js/pubsub.client.js"></script>

in your template.

Invoke the client using::

        pubsub = new PubSubClient({
                'nick': <unique_nick>,
                'node': '<node>',
                'event_cb': <callback to receive the events>
        });

or if you need authorized user to login, pass ``username`` and ``password`` instead of ``nick``

A simple event callback would be::

        function event_cb(entry, pubsub) {
            console.log("payload: ", $(entry).text());
            console.log("unread: ", pubsub.unread);
        }

The callback ``event_cb`` receives new updates. ``entry`` consists of the payload sent by
the publisher enclosed in a <entry> tag. ``pubsub`` is the instance of PubSubClient.

In addition you also have access to ``pubsub.unread`` which is the number of hits when the
window was not in focus, and ``pubsub.focus`` which is ``true`` if the window is active
else ``false``


*django-pubsub is web scale*
