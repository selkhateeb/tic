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
 * Array contains all the files added
 * 
 * @tyope {Array.<File>}
 */
example.client.file.FileComponent.prototype.files_ = [];

example.client.file.FileComponent.prototype.fragment = {
	DROP : 'd',
	IMAGES: 'i'
};

/**
 * Overrides the base.createDom method
 */
example.client.file.FileComponent.prototype.createDom = function() {
	this.element_ = this.getDomHelper().htmlToDocumentFragment(examples.client.file.template.root({
		id : this.makeId(this.fragment.DROP),
		images : this.makeId(this.fragment.IMAGES)
	}));
};
/**
 * Overrides the base.enterDocument method
 */
example.client.file.FileComponent.prototype.enterDocument = function() {
	goog.base(this, 'enterDocument');

	var drop = this.getElementByFragment(this.fragment.DROP);
	goog.events.listen(drop, goog.events.EventType.DRAGENTER, goog.bind(this.dropDragEnter_, this), false);
	goog.events.listen(drop, goog.events.EventType.DRAGLEAVE, goog.bind(this.dropDragLeave_, this));
	goog.events.listen(drop, goog.events.EventType.DRAGOVER, goog.bind(this.cancel_, this));
	goog.events.listen(drop, goog.events.EventType.DROP, goog.bind(this.dispatchFileReaderEvent_, this));

	goog.events.listen(this.getDomHelper().getDocument(), goog.events.EventType.DRAGENTER, goog.bind(this.bodyDragEnter_, this));
	goog.events.listen(this.getDomHelper().getDocument(), goog.events.EventType.DRAGLEAVE, goog.bind(this.bodyDragLeave_, this));
	goog.events.listen(this.getDomHelper().getDocument(), goog.events.EventType.DRAGOVER, goog.bind(this.cancel_, this));
	goog.events.listen(this.getDomHelper().getDocument(), goog.events.EventType.DROP, goog.bind(this.dispatchFileReaderEvent_, this));

    this.fileReader_.addEventListener(goog.fs.FileReader.EventType.LOAD_END, goog.bind(this.fileLoaded_, this));
};

example.client.file.FileComponent.prototype.dropDragEnter_ = function(e){
	e.preventDefault();
	goog.dom.classes.add(this.getElementByFragment(this.fragment.DROP), 'root_animate');
};
example.client.file.FileComponent.prototype.dropDragLeave_ = function(e){
	e.preventDefault();
	goog.dom.classes.remove(this.getElementByFragment(this.fragment.DROP), 'root_animate');
};

example.client.file.FileComponent.prototype.bodyDragEnter_ = function(e){
	e.preventDefault();
	goog.dom.classes.add(this.getElementByFragment(this.fragment.DROP), 'root_hover');
};
example.client.file.FileComponent.prototype.bodyDragLeave_ = function(e){
	// e.stopPropagation();
	e.preventDefault();
	if(e.clientX === 0 && e.clientY === 0){
	goog.dom.classes.remove(this.getElementByFragment(this.fragment.DROP), 'root_hover');
	}
};

example.client.file.FileComponent.prototype.cancel_ = function(e) {
	e.stopPropagation();
	e.preventDefault();
};

example.client.file.FileComponent.prototype.dispatchFileReaderEvent_ = function(e) {
	e.stopPropagation();
	e.preventDefault();
	goog.dom.classes.remove(this.getElementByFragment(this.fragment.DROP), 'root_hover');
	
	var dt = e.getBrowserEvent().dataTransfer;
	var file = dt.files[0];
	goog.array.extend(this.files_, dt.files);
    this.fileReader_.readAsDataUrl(file);
};



example.client.file.FileComponent.prototype.fileLoaded_ = function(e){
	console.log(e);
	var images = this.getElementByFragment(this.fragment.IMAGES);
	// var img = this.getDomHelper().createElement('img');
	// img.src = e.target.getResult();
	
	var node = this.getDomHelper().htmlToDocumentFragment(examples.client.file.template.image({
		imagedata : e.target.getResult()
	}));
	images.appendChild(node);
};

example.client.file.FileComponent.prototype.getImagesNode = function(){
  return this.getElementByFragment(this.fragment.IMAGES);
};
