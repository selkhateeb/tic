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
 * the Current Presenter displayed
 * @type {object}
 */
common.client.PlaceHistoryHandler.prototype.currentPresenter = null;

/**
 * @param {common.client.EventBus} eventBus
 * @param {common.client.Services} services
 */
common.client.PlaceHistoryHandler.prototype.register = function(eventBus, services, layoutManager){
    
    this.eventBus_ = eventBus;
    this.services_ = services;
    this.layoutManager_ = layoutManager;
    
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
    this.history_.setToken(place); //TODO: we can add readable title as second param
};

/**
 * Handles the history navigation event.
 * @param {goog.history.Event} event
 */
common.client.PlaceHistoryHandler.prototype.navigationEventHandler_ = function(event){
    var presenter = this.placeHistoryMapper_.getPresenter(event.token);
    if(this.currentPresenter){
	this.currentPresenter.hide();
    }

    var p = this.services_.getInjector().getInstance(presenter[0]);
    var args = [this.eventBus_].concat(presenter[1].slice(1));
    presenter[0].apply(p, args);
    
    p.bind();

    if(this.layoutManager_){
	this.layoutManager_.display(p);
    } else {
	p.display();
    }

    this.currentPresenter = p;

    //var placeChangeEvent = new common.client.place.PlaceChangeEvent(new place(event.token), this);
    //this.eventBus_.dispatchEvent(placeChangeEvent);
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
