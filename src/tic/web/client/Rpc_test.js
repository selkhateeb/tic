
goog.require('tic.web.client.Rpc');
goog.require('goog.testing.jsunit');

function test_createObjectUsingArray(){
    var rpc = new tic.web.client.Rpc();
    assertNotEquals(rpc.instance, null);
};

function test_exexute(){
    var rpc = new tic.web.client.Rpc();
    rpc.execute();
//    assertNotEquals(rpc.instance, null);
};

