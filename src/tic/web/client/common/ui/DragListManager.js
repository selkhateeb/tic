goog.provide('common.client.ui.DragListManager');

goog.require('goog.fx.DragListGroup');
goog.require('goog.ui.Dialog');

goog.require('tic');

//goog.require('receipty.client.receipt.editor.ReceiptComponent');

/**
 * @param {goog.dom.DomHelper=} opt_domHelper Optional DOM helper.
 * @constructor
 * @extends {goog.ui.Component}
 */
common.client.ui.DragListManager = function() {
	goog.base(this);
	
	this.addEventListener(goog.fx.DragListGroup.EventType.DRAGEND, goog.bind(this.event_,this));
	this.addEventListener(goog.fx.DragListGroup.EventType.DRAGMOVE, goog.bind(this.eventDragMove_,this));
	this.addEventListener(goog.fx.DragListGroup.EventType.BEFOREDRAGSTART, goog.bind(this.eventBeforeDragStart_,this));
	
	this.setHysteresis(1); //allows a click handler to be registered
};
goog.inherits(common.client.ui.DragListManager, goog.fx.DragListGroup);
tic.singleton(common.client.ui.DragListManager);

common.client.ui.DragListManager.prototype.clicked_ = function(e){
	console.log('clicked');
//	var component = new receipty.client.receipt.editor.ReceiptComponent();
//	component.render();
}

common.client.ui.DragListManager.prototype.event_ = function(e){
  goog.events.listen(e.currDragItem, goog.events.EventType.CLICK, this.clicked_, true, this);
  
};

common.client.ui.DragListManager.prototype.eventBeforeDragStart_ = function(e){
  var listeners = goog.events.getListeners(e.currDragItem, goog.events.EventType.CLICK, true);
  console.log(listeners);
  var len = listeners.length;
  for(i=0; i<len; i++){
  	goog.events.unlistenByKey(listeners[i]);
  }
  
};

common.client.ui.DragListManager.prototype.eventDragMove_ = function(e){
	if(!e.hoverList) return;
  dataId = e.hoverList.getAttribute('data-id');
  if(dataId)
  	e.currDragItem.status = dataId; 
};
common.client.ui.DragListManager.prototype.addElement = function(element){
  this.addElement_(element);
};

common.client.ui.DragListManager.prototype.addElement_ = function(element){
  
      var dragItem = element;
      var dragItemHandle = this.getHandleForDragItem_(dragItem);

      var uid = goog.getUid(dragItemHandle);
      this.dragItemForHandle_[uid] = dragItem;

      if (this.dragItemHoverClasses_) {
        this.eventHandler_.listen(
            dragItem, goog.events.EventType.MOUSEOVER,
            this.handleDragItemMouseover_);
        this.eventHandler_.listen(
            dragItem, goog.events.EventType.MOUSEOUT,
            this.handleDragItemMouseout_);
      }
      if (this.dragItemHandleHoverClasses_) {
        this.eventHandler_.listen(
            dragItemHandle, goog.events.EventType.MOUSEOVER,
            this.handleDragItemHandleMouseover_);
        this.eventHandler_.listen(
            dragItemHandle, goog.events.EventType.MOUSEOUT,
            this.handleDragItemHandleMouseout_);
      }

      this.dragItems_.push(dragItem);
      this.eventHandler_.listen(dragItemHandle,
          [goog.events.EventType.MOUSEDOWN, goog.events.EventType.TOUCHSTART],
          this.handlePotentialDragStart_);
};