goog.provide('common.client.PlaceManager');

goog.require('common.client.place.PlaceChangeEvent');

/**
 * @constructor
 * @param {common.client.EventBus} eventBus
 */
common.client.PlaceManager = function(eventBus){
    
    /**
     * Event bus
     * @type {common.client.EventBus}
     */
    this.eventBus_ = eventBus;
};

/**
 * @param {common.client.Place} place the place to go to 
 */
common.client.PlaceManager.prototype.goTo = function(place){
    this.eventBus_.dispatchEvent(new common.client.place.PlaceChangeEvent(place));
};

/**
 * @returns {common.client.EventBus} instance
 */
common.client.PlaceManager.prototype.getEventBus = function(){
    return this.eventBus_;
};

/**
 * Binds {common.client.Place} to its {common.client.Presenter}.
 */
common.client.PlaceManager.prototype.bind = goog.abstractMethod;
