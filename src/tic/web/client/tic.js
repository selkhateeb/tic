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

tic.INJECTION = {};

tic.inject = function(constructor, args) {
	tic.INJECTION[constructor] = {
		'constructor' : constructor,
		'args' : args
	};
};


tic.SINGLETON = {};
tic.SINGLETON_INSTANCES = {};

tic.singleton = function(constructor) {
	tic.SINGLETON[constructor] = 1;
};

tic.Injector = function(config){
	this.config = config;
};

tic.Injector.prototype.getInstance = function(constructor) {
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

tic.createInjector = function(module){
	module.buildConfig();
	return new tic.Injector(module.getConfigurations());
};

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

tic.AbstractModule = function() {
	this.config_ = {};
	this.configurations = {};
};
tic.AbstractModule.prototype.configure = goog.abstractMethod;
tic.AbstractModule.prototype.forConstructor = function(constructor) {
	return this.for_(constructor);
};

tic.AbstractModule.prototype.for_ = function(constructor) {
	if(!this.config_[constructor]) {
		this.config_[constructor] = [];
	}
	var binder = new tic.Bind();
	this.config_[constructor].push(binder);
	return binder;
};

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
}

tic.AbstractModule.prototype.getConfigurations = function(){
	return this.configurations;
}

tic.Bind = function() {
};
tic.Bind.prototype.bind = function(arg) {
	this.arg = arg;
	this.to = new tic.To();
	return this.to;
};
tic.To = function() {
};
tic.To.prototype.to = function(arg) {
	this.arg = arg;
}