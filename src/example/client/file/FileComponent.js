goog.provide('example.client.file.FileComponent');

goog.require('goog.ui.Component');
goog.require('goog.fs.FileReader');

goog.require('tic');

goog.require('examples.client.file.template');

tic.requireCss('example.client.file.style');

/**
 * @param {goog.dom.DomHelper=} opt_domHelper Optional DOM helper.
 * @constructor
 * @extends {goog.ui.Component}
 */
example.client.file.FileComponent = function(opt_domHelper) {
	goog.base(this, opt_domHelper);
};
goog.inherits(example.client.file.FileComponent, goog.ui.Component);

/**
 * FileReader object
 * 
 * @type {!goog.fs.FileReader}
 * @private
 */
example.client.file.FileComponent.prototype.fileReader_ = new goog.fs.FileReader();

/**
 * Overrides the base.createDom method
 */
example.client.file.FileComponent.prototype.createDom = function() {
	this.element_ = this.getDomHelper().createElement('div');
	
	this.element_.innerHTML = examples.client.file.template.root({
		id : 'wo'
	});
};

/**
 * Overrides the base.enterDocument method
 */
example.client.file.FileComponent.prototype.enterDocument = function() {
	goog.base(this, 'enterDocument');
	console.log('wohoo');
};
