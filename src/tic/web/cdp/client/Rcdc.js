goog.provide('tic.web.cdp.client.Rcdc');
goog.require('nanosn.cse.shared.Retrieve');
goog.require('goog.net.XhrIo');
goog.require('goog.json');
/**
 * Here is what I need to send: 
 *  A Command Object: { _cc_: 'nanosn.cse.shared.Retrieve',
 *                      query: 'avalon',
 *                      key: 'FSA2324WER234WR3432R32RWE324'}
 *
 *  And Get Back
 *  A Command Result Object: { _cc_: 'nanosn.cse.shared.RetrieveResult',
 *                             resultSet: {stuff ...},
 *                             count: 10,
 *                             key: 'KL3J4ROI34234KJLK32M4N'}
 */


/**
 * @constructor
 */
tic.web.cdp.client.Rcdc = function(){
    // var d = {
    //     _cc_ : 'nanosn.cse.shared.Retrieve',
    //     query: 'this is cool',
    //     key: null
    // };
    // this.instance = this.createInstance_(d);
};
tic.web.cdp.client.Rcdc.prototype.instance = null;

/**
 * @param {object} json_instance a json Command/Result instance.
 */
tic.web.cdp.client.Rcdc.prototype.createInstance_ = function(json_instance){
    
    //Split the command class into array
    // converts 'tic.web.client.Rpc' => ['tic', 'web', 'client', 'Rpc']
    var arr = json_instance._cc_.split('.');

    // instantiate the object
    // obj = window['tic']['web']['client']['Rpc']
    var obj = window;
    for (var i = 0; i < arr.length; i++) {
        obj = obj[arr[i]];
    }
    
    delete json_instance._cc_;

    var instance = new obj(json_instance);
    return instance;
};

tic.web.cdp.client.Rcdc.prototype.execute = function(command, result_handler){
    var json = goog.json.serialize(command);//command.toJSON();
    goog.net.XhrIo.send('/rcdc',
        function(e) {
            var xhr = /** @type {goog.net.XhrIo} */ (e.target);
            var result = goog.json.unsafeParse(xhr.getResponseText());
            result_handler(result);
        },
        'POST',
        json,
        {'Content-Type': 'application/json'}
    );
};