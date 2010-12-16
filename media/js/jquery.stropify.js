//(function($) {

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
         *subscribes user to given node
         */
        subscribe: function(node) {
            return this._conn.pubsub.subscribe(this._jid, settings.PUBSUB_SERVICE, 
                    node, {}, this._handle_event, this._handle_event);
        },


        /*
         *publishes items to node
         */
        publish: function(node, items) {
            return this._conn.pubsub.publish(this._jid, settings.PUBSUB_SERVICE,
                    node, items, this._handle_event);
        },


        /*
         *handles pubsub event
         */
        _handle_event: function(stanza_xml) {
            console.log(stanza_xml);
            return true;
        },

        /* callback fired before disconnect */
        _on_disconnect: function(status) {
            //this.leave();
        }

    };

    /* PubSubClient class that initializes 
     * event handlers, auto connects to the server
     * and auto joins 'room' of options
     *
     */
    function PubSubClient(options) {
        var that = this;
        this.options = options;
        var connection = that.connect(options.username, options.password);
    }

    //// TODO: return jquery element like a good plugin

    //$.fn.stropify = function(opts) {
        //var defaults = {
        //};
        //var options = $.extend(defaults, opts);
        //return new PubSubClient(options);
    //};

//})(jQuery);

