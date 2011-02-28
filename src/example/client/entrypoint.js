goog.provide('example.client.entrypoint');

goog.require('example.client.SimpleComponent');

/**
 * Static method .. could be instance method too..
 * ie: example.client.entrypoint.prototype.onModuleLoad
 */
example.client.entrypoint.onModuleLoad = function(){

    var component = new example.client.SimpleComponent();
    component.render();
}