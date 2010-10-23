dojo.provide("tic.web.client.bootstrap");
dojo.require("dojox.lang.aspect");
(function(){
    (function(){
        var cssCounter = 0;
        var cssInFlight = {};
        var cssInFlightIntvl = null;
        var cssStartTime = 0;
        var idPrefix = dojo._scopeName + "RequireCss";

        var _watchCssInFlight = function(){
            //summary: watches to make sure all css files have loaded.

            var stillWaiting = false;
            for(var param in cssInFlight){
                //Protect against bad JS modifying Object.prototype
                if(typeof param == "string" && param.indexOf(idPrefix) == 0){
                    console.debug(cssInFlight[param].sheet);
//                    if((dojo.isMoz || dojo.isSafari) && cssInFlight[param].sheet.cssRules){
//                        //Since moz and safari do not work with onload callbacks on the link
//                        //tag, see if the sheet and sheet.cssRules exist. If so, then assume
//                        //the css file has be loaded.
//                        delete cssInFlight[param];
//                    }else{
//                        stillWaiting = true;
//                    }
                }
            }

            if(stillWaiting){
                //Make sure we have not reached the timeout stage.
                var waitInterval = (dojo.config.cssWaitSeconds || 15) * 1000;
                if((cssStartTime + waitInterval) < (new Date()).getTime()){
                    var err = "Timed out waiting for css files: ";
                    for(param in cssInFlight){
                        err += cssInFlight[param].href + " ";
                    }
                    throw err;
                }
            }else{
                //All loaded. Clean up.
                console.debug("all done");
                clearInterval(cssInFlightIntvl);
                cssInFlightIntvl = null;
            }
        }

        dojo.requireCss = function(/*String*/resourceName){
            //summary: Converts the resource name ("some.thing") to a CSS URL
            //(http://some.domain.com/path/to/some/thing.css), then adds the CSS file
            //to the page. Full urls can be passed in (instead of a "some.thing" resourceName.
            //It also registers this CSS file with the dojo loader. This
            //means that if you do a dojo.addOnLoad() callback after calling this function,
            //the addOnLoad callback will not be fired until the CSS file has loaded.
            //Note that style sheets may be evaluated in a different order than the order
            //they appear in the DOM. If you want precise ordering of style rules, make
            //one call to this function, then in a dojo.addOnLoad() callback, load the other,
            //and repeat this call structure until you load all the stylesheets.
            //Example:
            //		dojo.requireCss("some.thing");
            //		dojo.requireCss("http://some.domain.com/path/to/some/thing.css");
            //
            console.debug("fsadsdfsffs");
            //Translate resource name to a file path
            var path = resourceName;
            if(path.indexOf("/") == -1){
                path = dojo._getModuleSymbols(resourceName).join("/") + '.css';
                path = ((path.charAt(0) == '/' || path.match(/^\w+:/)) ? "" : dojo.baseUrl) + path;
            }
            if(dojo.config.cacheBust){
                path += (path.indexOf("?") == -1 ? "?" : "&") + String(dojo.config.cacheBust).replace(/\W+/g,"");
            }

            //Create the link node
            var link = dojo.doc.createElement("link");
            link.id = idPrefix + (cssCounter++);
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = path;
            cssInFlight[link.id] = link;

            console.debug(link.id + " created");

            //Set up loader hooks.
            //TODO

            //Register the onload trigger, if supported.
//            if(!(dojo.isMoz || dojo.isSafari)){
                //IE and Opera, which support onload. A not test is used in the above if
                //since for moz and safari, those are the only ones that are tested to have
                //the sheet property that we will test in the inflight
                //watch, so want to match that test with the one used here.
                link.onload = function(){
                    console.debug(link.id + " loaded");
                    delete cssInFlight[link.id];

                    //Try to help break circular memory leaks.
                    link.onload = null;
                }
//            }

            //Attach the node to document.
            if(!this.headElement){
                this._headElement = document.getElementsByTagName("head")[0];

                //Head element may not exist, particularly in html
                //html 4 or tag soup cases where the page does not
                //have a head tag in it. Use html element, since that will exist.
                //Seems to be an issue mostly with Opera 9 and to lesser extent Safari 2
                if(!this._headElement){
                    this._headElement = document.getElementsByTagName("html")[0];
                }
            }
            console.debug(link.id + " adding to head");
            this._headElement.appendChild(link);

            //Start the inflight watch.
            cssStartTime = (new Date()).getTime();
            if(!cssInFlightIntvl){
                cssInFlightIntvl = setInterval(_watchCssInFlight, 100);
            }
        }
    })();
    // hijack the dojo.toJson method so that we can serialize dates
    var dateSerializer = {
        around: function(obj){
            return dateSerializerHandler(obj)
        }
    }

    // hijack the dojo.fromJson method so that we can serialize dates
    var dateDeSerializer = {
        around: function(json){
            return dateDeSerializerHandler(json)
        }
    }
    var dateDeSerializerHandler = function(json){
        return eval("(" + json + ")"); // Object
    }

    var dateSerializerHandler = function(it){
        if(it === undefined){
            return "undefined";
        }
        var objtype = typeof it;
        if(objtype == "number" || objtype == "boolean"){
            return it + "";
        }
        if(it === null){
            return "null";
        }
        if(dojo.isString(it)){
            return dojo._escapeString(it);
        }

        if(it instanceof Date){
            return it.getTime() + "";
        }
        // recurse
        var recurse = arguments.callee;
        // short-circuit for objects that support "json" serialization
        // if they return "self" then just pass-through...
        var newObj;
        var nextIndent = "";
        var tf = it.__json__||it.json;
        if(dojo.isFunction(tf)){
            newObj = tf.call(it);
            if(it !== newObj){
                return recurse(newObj);
            }
        }
        if(it.nodeType && it.cloneNode){ // isNode
            // we can't seriailize DOM nodes as regular objects because they have cycles
            // DOM nodes could be serialized with something like outerHTML, but
            // that can be provided by users in the form of .json or .__json__ function.
            throw new Error("Can't serialize DOM nodes");
        }

        var sep = "";
        var newLine = "";

        // array
        if(dojo.isArray(it)){
            var res = dojo.map(it, function(obj){
                var val = recurse(obj);
                if(typeof val != "string"){
                    val = "undefined";
                }
                return newLine + val;
            });
            return "[" + res.join("," + sep) + newLine + "]";
        }
        if(objtype == "function"){
            return null; // null
        }
        // generic object code path
        var output = [], key;
        for(key in it){
            var keyStr, val;
            if(typeof key == "number"){
                keyStr = '"' + key + '"';
            }else if(typeof key == "string"){
                keyStr = dojo._escapeString(key);
            }else{
                // skip non-string or number keys
                continue;
            }
            val = recurse(it[key]);
            if(typeof val != "string"){
                // skip non-serializable values
                continue;
            }
            // FIXME: use += on Moz!!
            //	 MOW NOTE: using += is a pain because you have to account for the dangling comma...
            output.push(newLine  + keyStr + ":" + sep + val);
        }
        return "{" + output.join("," + sep) + newLine + "}";
    };

    var aop = dojox.lang.aspect
    aop.advise(dojo, "toJson", dateSerializer);
    aop.advise(dojo, "fromJson", dateDeSerializer);
})();

