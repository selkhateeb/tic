
goog.require('tic.web.client.Rpc');
goog.require('goog.testing.jsunit');

function test_createObjectUsingArray(){
    var rpc = new tic.web.client.Rpc();
    assertNotEquals(rpc.instance, null);
};

