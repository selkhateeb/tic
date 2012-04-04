goog.provide('common.client.PlaceHistoryHandler');

goog.require('common.client.PlaceHistoryMapper');
goog.require('tic');
goog.require('goog.History');
goog.require('common.client.place.PlaceChangeEvent');

/**
 * @constructor
 * @param {goog.History} historyMechanism
 * @param {common.client.PlaceHistoryMapper} placeHistoryMapper
 */
common.client.PlaceHistoryHandler = function(historyMechanism, placeHistoryMapper){
    /**
     * @type {goog.History}
     */
    this.history_ = historyMechanism;

    /**
     * @type {common.client.PlaceHistoryMapper}
     */
    this.placeHistoryMapper_ = placeHistoryMapper;
};
tic.inject(common.client.PlaceHistoryHandler, [goog.History, common.client.PlaceHistoryMapper]);
tic.singleton(common.client.PlaceHistoryHandler);

/**
 * @param {common.client.EventBus} eventBus
 * @param {common.client.Services} services
 */
common.client.PlaceHistoryHandler.prototype.register = function(eventBus, services){
    
    this.eventBus_ = eventBus;
    this.services_ = services;
    eventBus.addEventListener(
	common.client.place.PlaceChangeEvent.TYPE,
	this.placeChangeEventHandler_, 
	false, this);
    
    goog.events.listen(
	this.history_, 
	goog.History.EventType.NAVIGATE, 
	this.navigationEventHandler_, 
	false, this);

};

/**
 * Handles the place change event.
 * @param {common.client.place.PlaceChangeEvent} event
 */
common.client.PlaceHistoryHandler.prototype.placeChangeEventHandler_ = function(event){
    if(event.source == this) return; // we fired the event
    var place = event.getPlace();
    this.history_.setToken(place.token); //TODO: we can add readable title as second param
};

/**
 * Handles the history navigation event.
 * @param {goog.history.Event} event
 */
common.client.PlaceHistoryHandler.prototype.navigationEventHandler_ = function(event){
    console.log(event.token);
    var place = this.placeHistoryMapper_.getComponent(event.token);
    var placeChangeEvent = new common.client.place.PlaceChangeEvent(new place(event.token), this);
    this.eventBus_.dispatchEvent(placeChangeEvent);
    new place().render();
};

/**
 * Handles the current location
 */
common.client.PlaceHistoryHandler.prototype.handleCurrentLocation = function(){
    this.history_.setEnabled(true);
};

/**
 * returns the mapper instance
 */
common.client.PlaceHistoryHandler.prototype.getMapper = function(){
    return this.placeHistoryMapper_;
};