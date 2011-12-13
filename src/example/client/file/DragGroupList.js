goog.provide('example.client.file.DragListManager');

goog.require('goog.fx.DragListGroup');


/**
 * @param {goog.dom.DomHelper=} opt_domHelper Optional DOM helper.
 * @constructor
 * @extends {goog.ui.Component}
 */
example.client.file.DragListManager = function() {
	goog.base(this);
	this.addEventListener(goog.fx.DragListGroup.EventType.DRAGEND, goog.bind(this.event_,this));
};
goog.inherits(example.client.file.DragListManager, goog.fx.DragListGroup);

example.client.file.DragListManager.prototype.event_ = function(e){
  e.currDragItem.blaaa = 'INFPROGREEEEESSSS';
  console.log(e);
  console.log(this.dragLists_);
  console.log({'bla':this.dragItems_[0]});
  console.log(this.dragItemForHandle_);
};
example.client.file.DragListManager.prototype.addElement = function(element){
  this.addElement_(element);
};

example.client.file.DragListManager.prototype.addElement_ = function(element){
  
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