goog.provide('example.client.layout.LayoutComponent');

goog.require('goog.ui.Component');
goog.require('goog.fx.DragListGroup');

goog.require('tic');

goog.require('examples.client.layout.template');

tic.requireCss('example.client.layout.style');

/**
 * @param {goog.dom.DomHelper=} opt_domHelper Optional DOM helper.
 * @constructor
 * @extends {goog.ui.Component}
 */
example.client.layout.LayoutComponent = function(leftComponent, opt_domHelper) {
	goog.base(this, opt_domHelper);
	
	this.left_ = new goog.ui.Component();
	this.addChild(this.left_, true);

	this.center_ = new goog.ui.Component();
	this.addChild(this.center_, true);

	this.right_ = new goog.ui.Component();
	this.addChild(this.right_, true);
	
	this.left_.addChild(leftComponent, true);
	
	 this.dragList_ = new goog.fx.DragListGroup();

	
};
goog.inherits(example.client.layout.LayoutComponent, goog.ui.Component);

example.client.layout.LayoutComponent.prototype.fragment = {
	LEFT: 'l'
};

/**
 * Overrides the base.createDom method
 */
example.client.layout.LayoutComponent.prototype.createDom = function() {
	this.element_ = this.getDomHelper().htmlToDocumentFragment(examples.client.layout.template.root({
		// id : this.makeId(this.fragment.DROP),
		// left : this.makeId(this.fragment.LEFT)
	}));
	
};

/**
 * Overrides the base.enterDocument method
 */
example.client.layout.LayoutComponent.prototype.enterDocument = function() {
	goog.base(this, 'enterDocument');
	goog.dom.classes.add(this.left_.getContentElement(), 'left');
	goog.dom.classes.add(this.center_.getContentElement(), 'center');
	goog.dom.classes.add(this.right_.getContentElement(), 'right');
	
	var images = this.left_.getChildAt(0).getImagesNode();
	this.dragList_.addDragList(images, goog.fx.DragListDirection.RIGHT);
	this.dragList_.init();
};
