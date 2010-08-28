dojo.provide("tic.web.cdp.tests.client.properties");
dojo.require("tic.web.client.Service");
dojo.require("tic.web.cdp.tests.shared.TestSelfReturnedCommand");

doh.register("tic.web.cdp.tests.client.properties",
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

                dohDeferred.errback(exception);
            }
        });
        return dohDeferred;
    },
    ]);