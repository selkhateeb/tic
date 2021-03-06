goog.provide('example.client.SimpleComponent');
goog.require('tic');
goog.require('goog.ui.Component');
goog.require('examples.client.template');
goog.require('tic.web.cdp.client.Rcdc');
goog.require('example.shared.IsLoggedInCommand');

/*
 * demonstrates how this components uses a css which will be included
 * automatically in the produced html
 */
tic.requireCss('example.client.css');

/**
 * @param {goog.dom.DomHelper=} opt_domHelper Optional DOM helper.
 * @constructor
 * @extends {goog.ui.Component}
 */
example.client.SimpleComponent = function(opt_domHelper){
//    goog.ui.Component.call(this, opt_domHelper);
    goog.base(this, opt_domHelper);
};
goog.inherits(example.client.SimpleComponent, goog.ui.Component);


/**
 * Overrides the base.createDom method
 */
example.client.SimpleComponent.prototype.createDom = function(){
    var div = this.getDomHelper().createElement('div');
    div.setAttribute('class', 'red');

    //Demonstrate how to use the template
    div.innerHTML = examples.client.template.helloWorld();
    this.element_ = div;
    this.isUserLoggedIn()
};

example.client.SimpleComponent.prototype.isUserLoggedIn = function(){
	var service = new tic.web.cdp.client.Rcdc();
	var self = this;
	
	service.execute(new example.shared.IsLoggedInCommand({
		'user': 'me'}), 
		function(result) {
			console.log(result);
		});
};
