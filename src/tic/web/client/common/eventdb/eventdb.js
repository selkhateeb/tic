goog.provide('common.client.EventDB');
goog.provide('common.client.EventDB.EventType');

goog.require('goog.events.EventTarget');

/** @fileoverview until we have official support for window.indexedDB we have to define the
 * following: 
 * 	var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB;
 *	if('webkitIndexedDB' in window) {
 *		window.IDBTransaction = window.webkitIDBTransaction;
 *		window.IDBKeyRange = window.webkitIDBKeyRange;
 *	}
 */

/**
 * @constructor
 * @param {indexedDB} indexedDB the HTML5 window.indexedDB object 
 *                    or similar interface implementation if not available
 * @extends {goog.events.EventTarget}
 */
common.client.EventDB = function(indexedDB){
    goog.base(this);
    this.indexedDB = indexedDB;
};
goog.inherits(common.client.EventDB, goog.events.EventTarget);
/**
 * @const
 * @type {string} name of database
 * NOTE: for some reason if DBNAME = 'eventdb' nothing works! 
 * 		 (tested on chrome only)
 */
common.client.EventDB.DBNAME = 'edb';

/**
 * @type {number} version of database automatically adjusted 
 * TODO: not sure if indexedDB version allows for number type but works on
 * 		 chrome for now
 */
common.client.EventDB.prototype.version = 0.0;

/**
 * @const
 * @type {string} object store name that holds 'common.client.EventDB.event' data
 */
common.client.EventDB.OBJECT_STORE_NAME = 'event';

/**
 * @type {window.IDBDatabase} holds the database instance once opened
 */
common.client.EventDB.prototype.db = null;

/**
 * All Events Dispatched by EventDB object
 */
common.client.EventDB.EventType = {
    /** Fired when eventdb is opened successfully */
    EVENTDB_OPENED_SUCCESS : 'eventdbopenedsuccess',
    /** Fired when eventdb is deleted */
    EVENTDB_DELETED: 'eventdbdeleted',
    
    /** Fired when object store created successfully */
    OBJECT_STORE_CREATED: 'objectstorecreated'
};

/**
 * general error handler
 * @param {Object} e event
 */
common.client.EventDB.prototype.onerror = function(){
    // TODO: better error handling 
    console.log("global error:" + e);
};

/**
 * opens the eventdb and inits the object store
 * @param {function} onsuccess success callback 
 */
common.client.EventDB.prototype.open = function() {
    var request = this.indexedDB.open(common.client.EventDB.DBNAME);
    request.onsuccess = goog.bind(this.onOpenSuccess_,this);
    request.onerror = this.onerror;
};

/**
 * This function gets called when the DB opens successfuly
 * @param {} e TODO: Find the type from indexedDB docs
 * @see {open}
 */
common.client.EventDB.prototype.onOpenSuccess_ = function(e){
    this.db = e.target.result;
    
    if(this.version === this.db.version) return; //we already have it setup

    this.createObjectStore_(
	common.client.EventDB.OBJECT_STORE_NAME,
	{keyPath: "when"});

    this.dispatchEvent(new goog.events.Event(common.client.EventDB.EventType.EVENTDB_OPENED_SUCCESS));
};

/**
 * creates the named object store
 * @param {string} name name of object store to be created
 * @param {object} options object store options
 * @private
 */
common.client.EventDB.prototype.createObjectStore_ = function(name, options, deleteIfExist_opt){

    // We can only create Object stores in a setVersion transaction;
    this.version += 0.1;
    var setVrequest = this.db.setVersion(this.version);
    
    // onsuccess is the only place we can create Object Stores
    setVrequest.onerror = this.onerror;
    setVrequest.onsuccess = goog.bind(function(e) {
	if(deleteIfExist_opt && this.db.objectStoreNames.contains(name)) {
	    this.db.deleteObjectStore(name);
	}
	var store = this.db.createObjectStore(name, options);
	this.dispatchEvent(new goog.events.Event(common.client.EventDB.EventType.OBJECT_STORE_CREATED));
    }, this);
};

/**
 * deletes the eventdb databese
 */
common.client.EventDB.prototype.deletedb = function() {
    if(!this.indexedDB.deleteDatabase){
	console.warn("indexedDB.deleteDatebase not supported yet");
	return;
    }
    var request = this.indexedDB.deleteDatabase(common.client.EventDB.DBNAME);
    request.onsuccess = goog.bind(function(e) {
	    this.dispatchEvent(new goog.events.Event(common.client.EventDB.EventType.EVENTDB_DELETED));
    }, this);
    request.onerror = goog.bind(this.onerror, this);
};


/**
 * adds an event to object store
 * @param {common.client.EventDB.event} event event object
 * @param {function} onsuccess success callback
 * @param {function} onerror error callback
 */
common.client.EventDB.prototype.putEvent = function(event, onsuccess, onerror) {
    var trans = this.db.transaction([common.client.EventDB.OBJECT_STORE_NAME], IDBTransaction.READ_WRITE);

    var store = trans.objectStore(common.client.EventDB.OBJECT_STORE_NAME);
    var request = store.put(event);
    request.onsuccess = onsuccess;
    request.onerror = onerror;
};

/**
 * deletes the event by id
 * @param {string|number} id event id/key
 */
common.client.EventDB.prototype.deleteEvent = function(id) {
    var db = this.db;
    var trans = db.transaction([common.client.EventDB.OBJECT_STORE_NAME], IDBTransaction.READ_WRITE);
    var store = trans.objectStore(common.client.EventDB.OBJECT_STORE_NAME);

    var request = store.delete(id);
    var THIS = this;
    request.onsuccess = function(e) {
	THIS.getAllEvents();
    };
    request.onerror = function(e) {
	console.log("Error Deleting: ", e);
    };
};

/**
 * gets all events from database
 * @param {function} onevent fires on every result record
 */
common.client.EventDB.prototype.getAllEvents = function(onevent) {
    var db = this.db;
    var trans = db.transaction([common.client.EventDB.OBJECT_STORE_NAME], IDBTransaction.READ_WRITE);
    var store = trans.objectStore(common.client.EventDB.OBJECT_STORE_NAME);

    // Get everything in the store;
    var keyRange = IDBKeyRange.lowerBound(0);
    var cursorRequest = store.openCursor(keyRange);

    cursorRequest.onsuccess = function(e) {
	var result = e.target.result;
	if(!!result == false)
	    return;

	onevent(result.value);
	result.continue();
    };
    cursorRequest.onerror = this.onerror;
};

/**
 * gets all objects from database
 * @param {string} storeName the name of the store to get all data 
 * @param {function} onrecord fires on every result record
 */
common.client.EventDB.prototype.getAll = function(storeName, onrecord) {
    var trans = this.db.transaction([storeName], IDBTransaction.READ_ONLY);
    var store = trans.objectStore(storeName);

    // Get everything in the store;
    var keyRange = IDBKeyRange.lowerBound(0);
    var cursorRequest = store.openCursor(keyRange);

    cursorRequest.onsuccess = function(e) {
	var result = e.target.result;
	if(!result)
	    return;

	onrecord(result.value);
	result.continue();
    };
    cursorRequest.onerror = this.onerror;
};

/**
 * applys local changes
 */
common.client.EventDB.prototype.apply = function(onsuccess){
    var self = this;
    this.getAllEvents(function(e){
  	self.applyInternal_(e, onsuccess);
    });
};

/**
 * applys local changes
 * @param {common.client.EventDB.event} event event record
 * @private
 */
common.client.EventDB.prototype.applyInternal_ = function(event, onsuccess){
    if(event.what.operation === 'put'){
	this.handlePutOperation_(event.what.store, event.what.changed_to, onsuccess);
    }
    this.deleteEvent(event.when);
};

common.client.EventDB.prototype.handlePutOperation_ = function(store_name, object, onsuccess){
    console.log("store name", store_name);
    var self = this;
    if(!this.db.objectStoreNames.contains(store_name)){
	this.createObjectStore_(store_name, {autoIncrement: true, keyPath: 'id'}, function(){
	    self.handlePutOperation_(store_name, object);
	});
	return;
    }
    var trans = this.db.transaction([store_name], IDBTransaction.READ_WRITE);
    console.log(trans);
    var store = trans.objectStore(store_name);

    var request = store.put(object);

    request.onsuccess = function(e){
	console.log('handleputSuccess', e);
	onsuccess(e);
    };
    request.onerror = function(e){
	console.log('handleputError', e);
    };

};
