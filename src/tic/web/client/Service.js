/**
 *
 */
dojo.provide("tic.web.client.Service");
dojo.require("dojox.rpc.Service");
dojo.require("dojox.rpc.JsonRPC");

dojo.declare(
    "tic.web.client.Service",
    null,
    {
        _service: new dojox.rpc.Service({
            envelope:"JSON-RPC-2.0",
            transport:"POST",
            target:"/rpc",
            services:{
                "tic.web.cdp.main.CommandDispatcher.execute":{}
            }
        }),

        // Args:
        //      scope: optional
        execute: function(command, scope, callbackFunction){
            //Do the optional magic
            if(arguments.length == 2){
                callbackFunction = scope;
                scope = null;
            }
            
            var deferred = this._service.tic.web.cdp.main.CommandDispatcher.execute(command);
            if(callbackFunction)
                deferred.addCallback(dojo.hitch(scope, callbackFunction));
            return deferred
        }
    });