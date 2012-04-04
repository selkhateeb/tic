goog.provide('common.client.place.PlaceChangeEvent');

goog.require('goog.events.Event');

/**
 * @constructor
 * @param {common.client.Place} place
 * @param {=object} opt_source the source of event
 * @extends {goog.events.Event}
 */
common.client.place.PlaceChangeEvent = function(place, opt_source){
    goog.base(this, common.client.place.PlaceChangeEvent.TYPE);

    /**
     * @type {common.client.Place}
     */
    this.place_ = place;
    
    /**
     * @type {object|null}
     */
    this.source = opt_source;
};
goog.inherits(common.client.place.PlaceChangeEvent, goog.events.Event);

/**
 * Event type.
 * @type {string}
 */
common.client.place.PlaceChangeEvent.TYPE = 'PlaceChangeEvent';


/**
 * @returns {common.client.Place} the place
 */
common.client.place.PlaceChangeEvent.prototype.getPlace = function(){
    return this.place_;
};
