
goog.require('common.client.EventDB');
goog.require('common.client.EventDB.EventType');
goog.require('common.client.eventdb.Event');
goog.require('goog.testing.AsyncTestCase');
goog.require('goog.testing.jsunit');
goog.require('tic.coverage');

var eventdb = null;
var indexedDB = window.indexedDB || window.webkitIndexedDB || window.mozIndexedDB;
if('webkitIndexedDB' in window) {
    window.IDBTransaction = window.webkitIDBTransaction;
    window.IDBKeyRange = window.webkitIDBKeyRange;
}

function setUp(){
    eventdb = new common.client.EventDB(indexedDB);
};

function testConstructor(){
    assertEquals(indexedDB, eventdb.indexedDB);
};

function testOpen(){
    function callback(){
	asyncTestCase.continueTesting();
    };
    asyncTestCase.waitForAsync();

    goog.events.listen(
	eventdb, 
	common.client.EventDB.EventType.EVENTDB_OPENED_SUCCESS, 
	callback);
    eventdb.open();
};

function testPutEvent(){
    var e = new common.client.eventdb.Event();
    function s(ev){
	console.log(ev);
	asyncTestCase.continueTesting();
    };
    function f(ev){
	fail("something went wrong putting event");
    }
    asyncTestCase.waitForAsync();

    goog.events.listen(
	eventdb,
	common.client.EventDB.EventType.EVENTDB_OPENED_SUCCESS,
	callback);
    eventdb.open();

    eventdb.putEvent(e, s,f);
}

function testDeletedb(){
    function callback(){
	asyncTestCase.continueTesting();
    };
    asyncTestCase.waitForAsync();

    goog.events.listen(
	eventdb, 
	common.client.EventDB.EventType.EVENTDB_DELETED, 
	callback);
    eventdb.deletedb();
};


var asyncTestCase = goog.testing.AsyncTestCase.createAndInstall();
