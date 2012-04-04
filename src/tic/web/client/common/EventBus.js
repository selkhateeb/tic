goog.provide('common.client.EventBus');

goog.require('tic');

goog.require('goog.events.EventTarget');

/**
 * Default implementation of EventBus
 *
 * @constructor
 * @extends {goog.events.EventTarget}
 */
common.client.EventBus = function(){
  goog.events.EventTarget.call(this);	
}
goog.inherits(common.client.EventBus, goog.events.EventTarget);
tic.singleton(common.client.EventBus);
