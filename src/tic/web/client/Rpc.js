goog.provide('tic.web.client.Rpc');
goog.require('nanosn.cse.shared.Retrieve');
goog.require('goog.net.XhrIo');
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
tic.web.client.Rpc = function(){
    var d = {
        _cc_ : 'nanosn.cse.shared.Retrieve',
        query: 'this is cool',
        key: null
    };
    this.instance = this.createInstance_(d);
};
tic.web.client.Rpc.prototype.instance = null;

/**
 * @param {object} json_instance a json Command/Result instance.
 */
tic.web.client.Rpc.prototype.createInstance_ = function(json_instance){
    
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
}