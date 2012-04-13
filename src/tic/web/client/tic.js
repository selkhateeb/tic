goog.provide('tic');
goog.provide('tic.AbstractModule');

goog.require('goog.array');

tic.bind = Function.prototype.bind || function (oThis) {
    if (typeof this !== "function") {  
	// closest thing possible to the ECMAScript 5 internal IsCallable function  
	throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");  
    }
    var aArgs = Array.prototype.slice.call(arguments, 1),   
    fToBind = this,   
    fNOP = function () {},  
    fBound = function () {
	return fToBind.apply(this instanceof fNOP
			     ? this
			     : oThis || window,
			     aArgs.concat(Array.prototype.slice.call(arguments)));
    };
    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();
    return fBound;
};




/*
 * A marker method for the builder to request css resources from within the
 * javascript.
 * adds the required link tag in the head of the requested url
 *
 * used with the css at-rule @tic.provide
 *
 * @param {String} rule The rule package .. similar to goog.require
 */
tic.requireCss = function(rule) {

};

/**
 * Global object for registering all tic.inject statments
 */
tic.INJECTION = {};

/**
 * similar to @inject for in google guice
 * @param {constructor} constructor
 * @param {array.<constructor>} args
 */
tic.inject = function(constructor, args) {
    tic.INJECTION[goog.getUid(constructor)] = new tic.Injector.Type(constructor, args);
};

/**
 * Global object for registering all singleton signitures
 */
tic.SINGLETON = {};

/**
 * Global object for holding all singleton instances
 * 
 */
tic.SINGLETON_INSTANCES = {};

/**
 * Register a singleton class
 * TODO: see the possibility of using goog singleton thingy
 * @param {class|constructor} constructor
 */
tic.singleton = function(constructor) {
    tic.SINGLETON[goog.getUid(constructor)] = 1;
};

/**
 * Injector class for managing deps
 * @constructor
 * @param {tic.AbstractModule} config
 */
tic.Injector = function(config, providers){
    this.config = config;

    /**
     * @type {object}
     */
    this.providers = providers;
    
    //add us to the singleton world
    tic.SINGLETON_INSTANCES[goog.getUid(tic.Injector)] = this;
};
tic.singleton(tic.Injector);

/**
 * @returns {object} new instance of the class
 * @param {class|constructor} constructor
 */
tic.Injector.prototype.getInstance = function(constructor) {
    if(!goog.isDef(constructor))
	throw 'Cannot create instance of ' + constructor + ' did you forget goog.require?';
    
    var provided = this.getProvidedInstance_(constructor);
    if(provided) return provided;
    var type = tic.INJECTION[goog.getUid(constructor)];
    if(!type) {
	//assume we dont have arguments
	return tic.createInstance_(constructor);
    }

    var instances = [constructor];
    for( var i = 0; i < type.args.length; i++) {
	if(this.config[goog.getUid(constructor)])
	    var t = this.config[goog.getUid(constructor)][goog.getUid(type.args[i])];
	if(t)
	    var ins = this.getInstance(t, this.config);
	else
	    var ins = this.getInstance(type.args[i], this.config);
	instances.push(ins);
    }
    var instance = tic.createInstance_(constructor, instances);
    return instance;
};

/**
 * creates an instace from a provided method
 * @param {class|constructor} constructor
 */
tic.Injector.prototype.getProvidedInstance_ = function(constructor){
    var provider = this.providers[goog.getUid(constructor)];
    if(!provider) return null;
    var provider_instance = this.getInstance(provider);
    return provider_instance.get();
};

/**
 * @constructor
 * @param {object} constructor
 * @param {Array.<object>} args
 */
tic.Injector.Type = function(constructor, args){
    /**
     * @type {object}
     */
    this.constructor = constructor;
    /**
     * @type {Array.<object>}
     */
    this.args = args;
};



/**
 * Creates an Injector instance
 * @param {tic.AbstractModule} module
 */
tic.createInjector = function(module){
    module.buildConfig();
    return new tic.Injector(module.getConfigurations(), module.getProviders());
};

/**
 * creates instance for the provided class along with its args
 */
tic.createInstance_ = function(constructor, args) {
    if(tic.SINGLETON[goog.getUid(constructor)]) {
	//check if we have instantiated it already
	var instance = tic.SINGLETON_INSTANCES[goog.getUid(constructor)];
	if(!instance) {
	    instance = new (tic.bind.apply(constructor,args));
	    tic.SINGLETON_INSTANCES[goog.getUid(constructor)] = instance;
	}
	return instance;
    }
    return new (tic.bind.apply(constructor,args));
};

/**
 * Abstract module for configuring the injector
 * @constructor
 */
tic.AbstractModule = function() {
    this.config_ = {};
    this.configurations = {};
    
    /**
     * @type {object}
     */
    this.providers_signitures_ = {};
    
    /**
     * @type {object}
     */
    this.providers_ = {};
};

/**
 * Abstract method that contains all the bindings
 */
tic.AbstractModule.prototype.configure = goog.abstractMethod;

/**
 * the starting point for binding
 * @param {class|constructor} constructor
 * @returns {tic.Bind}
 */
tic.AbstractModule.prototype.forConstructor = function(constructor) {
    return this.for_(constructor);
};

/**
 * Binds to a Provider
 */
tic.AbstractModule.prototype.bind = function(constructor){
    this.providers_signitures_[goog.getUid(constructor)] = new tic.ProviderBinding();
    return this.providers_signitures_[goog.getUid(constructor)];
};

/**
 * helper for forConstructor method
 * @returns {tic.Bind}
 */
tic.AbstractModule.prototype.for_ = function(constructor) {
    if(!this.config_[goog.getUid(constructor)]) {
	this.config_[goog.getUid(constructor)] = [];
    }
    var binder = new tic.Bind();
    this.config_[goog.getUid(constructor)].push(binder);
    return binder;
};

/**
 * Builds the configuration object as defined in configure method
 */
tic.AbstractModule.prototype.buildConfig = function() {
    this.configure();
    for(var c in this.config_) {
	var binders = this.config_[c];
	var b = {};
	for( var i = 0; i < binders.length; i++) {
	    var binder = binders[i];
	    b[goog.getUid(binder.arg)] = binder.to.arg;
	}
	this.configurations[c] = b;
    }
    
    for(var p in this.providers_signitures_){
	var provider = this.providers_signitures_[p];
	this.providers_[p] = provider.provider;
    }
}

/**
 * @returns {object} the configurations object
 */
tic.AbstractModule.prototype.getConfigurations = function(){
	return this.configurations;
}

/**
 * @returns {object} the provider configurations object
 */
tic.AbstractModule.prototype.getProviders = function(){
    return this.providers_;
}

/**
 * @constructor
 */
tic.Bind = function() {};

/**
 * Binds class
 * @param {class|constructor} arg
 */
tic.Bind.prototype.bind = function(arg) {
	this.arg = arg;
	this.to = new tic.To();
	return this.to;
};

/**
 * @constructor
 */
tic.To = function() {};

/**
 * the to part of binding
 * @param {class|constructor} arg
 */
tic.To.prototype.to = function(arg) {
	this.arg = arg;
}

/**
 * @constructor
 */
tic.ProviderBinding = function(){};

/**
 * Binding to provider
 * @param {tic.Provider} provider
 */
tic.ProviderBinding.prototype.toProvider = function(provider){
    this.provider = provider;
};

goog.provide('tic.Provider');

/**
 * @interface
 */
tic.Provider = function(){};

/**
 * @returns an instance of the provided objcet
 */
tic.Provider.prototype.get = function(){};

