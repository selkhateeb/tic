dojo.provide("tic.client.Loading");
dojo.require("dijit._Widget");
dojo.require("dijit._Templated");

dojo.declare("tic.client.Loading",
    [dijit._Widget, dijit._Templated], {
        imageUrl: dojo.moduleUrl('tic.client','resources/images/loading.gif').path,
        templateString: '<img src="${imageUrl}"/>'
    });