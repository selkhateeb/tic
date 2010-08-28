dojo.provide("tic.web.cdp.tests.client.module");
dojo.require("tic.web.client.Service");
dojo.require("tic.web.cdp.tests.shared.TestSelfReturnedCommand");

doh.register("tic.web.cdp.tests.client.module",
    [
    function test_stringProperty(doh){
        var dohDeferred = new doh.Deferred();
        var service = new tic.web.client.Service();
        var expected = "sweet";
        var command = new tic.web.cdp.tests.shared.TestSelfReturnedCommand({
            string: expected
        });
        
        service.execute(command, this, function(result){
            try {
                doh.is(expected, result.string);
                dohDeferred.callback(true);
            } catch (exception) {

                dohDeferred.errback(new Error(exception.message));
            }


        });
        return dohDeferred;
    },
    function test_success(doh){
        doh.is('a', 'a');
    },
    function test_fail(doh){
        doh.is('a', 'b');
    }
    ]);