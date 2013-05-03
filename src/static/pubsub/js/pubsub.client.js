/*
 *This program is distributed under the terms of the MIT license.
 *Please see the LICENSE file for details.
 *
 *Copyright Agiliq Solutions
 *
 */

PubSubClient.prototype = {

    /* connect to the xmpp server
    *
    * params:
    *
    *   username: username of xmpp account without domain
    *   password: plaintext password of the account
    *
    * for anonymous logins
    *
    *   nick: the nickname to be displayed after anoymous login
    *
    * returns:
    *   Strophe.Connection object
    */
    connect: function(username, password) {
        this._conn = new Strophe.Connection(settings.BOSH_SERVICE);
        this._jid = this._nick + '@' + settings.DOMAIN + '/' + settings.RESOURCE;
        if ( typeof(username) != 'undefined' &&  username.length) {
            this._conn.connect(this._jid, password, this._on_connect(this));
            this._nick = username;
        }
        else {
            // anonymous login
            this._conn.connect(settings.DOMAIN, null, this._on_connect(this));
            this._nick = this.options.nick;
        }
        return this._conn;
    },

    /*
     * Alternative to connect, using BOSH session id
     *
     * See: http://metajack.im/2008/10/03/getting-attached-to-strophe/
     *
     */
    attach: function(jid, sid, rid) {
        this._conn = new Strophe.Connection(settings.BOSH_SERVICE);
        this._jid = jid;
        this._nick = this._jid.split("@")[0];
        return this._conn.attach(jid, sid, rid, this._on_connect(this));
    },

    /* disconnect from the xmpp server */
    disconnect: function() {
        this._conn.disconnect();
        this._on_disconnect();
    },

    /* callback fired when connection status changes */
    _on_connect: function(context) {
        return function (status, condition) {
            context._jid = context._conn.jid;
            if (settings.DEBUG) {
                console.log("status is ", status);
            }
                if (status == Strophe.Status.CONNECTED) {
                context.subscribe(context.options.node); // FIXME: subscribe only once
            }
        };
    },

    /*
    *publishes items to node
    */
    publish: function(node, items) {
        return this._conn.pubsub.publish(this._jid, settings.PUBSUB_SERVICE,
                node, items, this._handle_event(this));
    },

    /*
    *subscribes user to given node
    */
    subscribe: function(node) {
        return this._conn.pubsub.subscribe(this._jid, settings.PUBSUB_SERVICE,
                node, {}, this._handle_event(this), this._handle_event(this));
    },

    /*
    *handles pubsub event
    */
    _handle_event: function(context) {
        return function(stanza_xml) {
            if (settings.DEBUG) {
                console.log(stanza_xml);
            }
            entry = $(stanza_xml).find("entry");
            if (entry.length) {
                context.updates.push(entry);
                context.options.event_cb(entry, context);
            }
            return true;
        };
    },

    /* callback fired before disconnect */
    _on_disconnect: function(status) {
    },

    focus: true, /* whether the window has focus */
    unread: 0 /* count of unread messages */

};

/* PubSubClient class that initializes
* event handlers, connects to the server
*
* Login Options:
*
* username: xmpp account username (without domain)
* password: xmpp account password
*
* or
*
* nick: nick for anonymous login
*
*
* PUBSUB Options:
*
* node: the node to subscribe and listen for updates
* event_cb: callback fired when an event occurs in the
* subscribed node. Has entry with payload as first argument
* and PubSub object as second argument
*
*/
function PubSubClient(options) {
    this.options = options;
    this.updates = new Array();
    var connection = null;
    if (typeof(options.jid) != 'undefined' &&  options.jid.length) {
        connection = this.attach(options.jid, options.rid, options.sid);
    }
    else {
        connection = this.connect(options.username, options.password);
    }

    $(window).blur(function(context) {
        return function() {
            context.focus = false;
        };
    }(this));

    $(window).focus(function(context) {
        return function() {
            context.focus = true;
            /* reset counter */
            context.unread = 0;
        };
    }(this));

}

