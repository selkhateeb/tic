
goog.require('tic.web.cdp.client.Rcdc');
goog.require('goog.testing.jsunit');

function test_createObjectUsingArray(){
    var rpc = new tic.web.cdp.client.Rcdc();
    assertNotEquals(rpc.instance, null);
};

function test_exexute(){
    var rpc = new tic.web.cdp.client.Rcdc();
    var command = new nanosn.cse.shared.Retrieve({query:'bla', key: ''});
    rpc.execute(command);
//    assertNotEquals(rpc.instance, null);
};

