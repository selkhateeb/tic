goog.provide('common.client.eventdb.Event');

/**
 * @constructor
 */
common.client.eventdb.Event = function(){
    this.when = new Date().getTime();
};

/**
 * @type {Number} timestamp when the event happened
 */
common.client.eventdb.Event.prototype.when = null;

/**
 * @type {*} who did this event
 * example: user name, user object, id , etc ...
 */
common.client.eventdb.Event.prototype.who = null;

/**
 * @type {Object} what happend 
 * example:
 * 		this is what an object looks like when we try to change
 * 		the value of a todo item from 'hmm' to 'drink water'
 * 		{  
 * 			store: 'todos',
 * 			property: 'text',
 *          operation: 'put',
 * 			key: 1243421432,
 * 			changed_from: 'hmm',
 * 			changed_to: 'drink water'
 * 		}
 */
common.client.eventdb.Event.prototype.what = null;

/**
 * @type {*} where did the event take place
 * examples: 
 * 		mobile, browser, url, etc ...
 */
common.client.eventdb.Event.prototype.where = null;//url, browser, mobile

/**
 * @type {*} how did it happen
 * examples:
 * 		- user clicked button/link
 *		- user hit key
 * 		- backend process
 * 		- etc..
 */
common.client.eventdb.Event.prototype.how = null;
