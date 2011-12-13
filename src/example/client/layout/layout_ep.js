goog.provide('example.client.layout.layout_ep');

// goog.require('example.client.SimpleComponent');
goog.require('example.client.file.FileComponent');
goog.require('example.client.layout.LayoutComponent');
goog.require('example.client.file.DragListManager');
/**
 * Static method .. could be instance method too..
 * ie: example.client.entrypoint.prototype.onModuleLoad
 */
example.client.layout.layout_ep.onModuleLoad = function(){


    
    var dragListManager = new example.client.file.DragListManager();
    
    var fileComponent = new example.client.file.FileComponent(dragListManager);
    var layout = new example.client.layout.LayoutComponent(
    	dragListManager,
    	fileComponent);
    layout.render();
    dragListManager.init();

}