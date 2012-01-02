goog.provide('tic');
goog.provide('tic.AbstractModule');

goog.require('goog.array');
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
    tic.INJECTION[constructor] = {
	'constructor' : constructor,
	'args' : args
    };
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
    tic.SINGLETON[constructor] = 1;
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
    tic.SINGLETON_INSTANCES[tic.Injector] = this;
};
tic.singleton(tic.Injector);

/**
 * @returns {object} new instance of the class
 * @param {class|constructor} constructor
 */
tic.Injector.prototype.getInstance = function(constructor) {
    var provided = this.getProvidedInstance_(constructor);
    if(provided) return provided;
    var type = tic.INJECTION[constructor];
    if(!type) {
	//assume we dont have arguments
	return tic.createInstance_(constructor);
    }

    var instances = [constructor];
    for( i = 0; i < type.args.length; i++) {
	if(this.config[constructor])
	    var t = this.config[constructor][type.args[i]];
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
    var provider = this.providers[constructor];
    if(!provider) return null;
    var provider_instance = this.getInstance(provider);
    return provider_instance.get();
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
    if(tic.SINGLETON[constructor]) {
	//check if we have instantiated it already
	var instance = tic.SINGLETON_INSTANCES[constructor];
	if(!instance) {
	    instance = new (constructor.bind.apply(constructor,args))();
	    tic.SINGLETON_INSTANCES[constructor] = instance;
	}
	return instance;
    }
    return new (constructor.bind.apply(constructor,args))();
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
    this.providers_signitures_[constructor] = new tic.ProviderBinding();
    return this.providers_signitures_[constructor];
};

/**
 * helper for forConstructor method
 * @returns {tic.Bind}
 */
tic.AbstractModule.prototype.for_ = function(constructor) {
    if(!this.config_[constructor]) {
	this.config_[constructor] = [];
    }
    var binder = new tic.Bind();
    this.config_[constructor].push(binder);
    return binder;
};

/**
 * Builds the configuration object as defined in configure method
 */
tic.AbstractModule.prototype.buildConfig = function() {
    this.configure();
    for(c in this.config_) {
	var binders = this.config_[c];
	var b = {};
	for( i = 0; i < binders.length; i++) {
	    var binder = binders[i];
	    b[binder.arg] = binder.to.arg;
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

