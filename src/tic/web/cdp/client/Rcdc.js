goog.provide('tic.web.cdp.client.Rcdc');
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
 * @implements {tic.web.cdp.client.IRcdc}
 */
tic.web.cdp.client.Rcdc = function(){};
tic.web.cdp.client.Rcdc.prototype.execute = function(command, result_handler){
    var json = goog.json.serialize(command);
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