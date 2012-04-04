goog.provide('common.client.PlaceHistoryMapper');
goog.provide('common.client.PlaceHistoryMapper.Mapper');

/**
 * @constructor
 */
common.client.PlaceHistoryMapper = function(){
};


/**
 * holds a list of all the mappings added.
 * @type {Array} common.client.PlaceHistoryMapper.Mapper
 */
common.client.PlaceHistoryMapper.prototype.mappings_ = [];

/**
 * maps history token regex
 * @param {string} token_regex
 */
common.client.PlaceHistoryMapper.prototype.map = function(token_regex){
    var mapper = new common.client.PlaceHistoryMapper.Mapper(token_regex);
    this.mappings_.push(mapper);
    return mapper;
};

/**
 * returns the component class
 */
common.client.PlaceHistoryMapper.prototype.getComponent = function(token){
    var len = this.mappings_.length;
    for( var i=0; i < len; i++){
	var mapper = this.mappings_[i];
	if(mapper.token.test(token))
	    return mapper.component;
    }
};

/**
 * @constructor
 * @param {string} token History token
 */
common.client.PlaceHistoryMapper.Mapper = function(token){
    /**
     * @type {RegExp}
     */
    this.token = token;
};

common.client.PlaceHistoryMapper.Mapper.prototype.token = null;
common.client.PlaceHistoryMapper.Mapper.prototype.component = null;

/**
 * the place that the history token should be mapped to
 * @param {goog.ui.Component} component for now
 */
common.client.PlaceHistoryMapper.Mapper.prototype.to = function(component){
    this.component = component;
};
