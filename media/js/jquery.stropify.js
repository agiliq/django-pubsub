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
        this._jid = username + '@' + settings.DOMAIN + '/' + settings.RESOURCE;
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

    /* disconnect from the xmpp server */
    disconnect: function() {
        this._conn.disconnect();
        this._on_disconnect();
    },

    /* callback fired when connection status changes */
    _on_connect: function(context) {
        return function (status, condition) {
            if (settings.DEBUG) {
                console.log("status is ", status);
            }
                if (status == Strophe.Status.CONNECTED) {
                context.subscribe(context.options.node);
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
                context.options.event_cb(entry);
            }
            return true;
        };
    },

    /* callback fired before disconnect */
    _on_disconnect: function(status) {
    }

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
* subscribed node. Takes a single argument which is the
* payload enclosed in <entry> xml element
*
*/
function PubSubClient(options) {
    this.options = options;
    this.updates = new Array();
    var connection = this.connect(options.username, options.password);
}

