goog.provide('example.client.entrypoint');

goog.require('goog.editor.Field');

/**
 * Static method .. could be instance method too..
 * ie: example.client.entrypoint.prototype.onModuleLoad
 */
example.client.entrypoint.onModuleLoad = function(){
    document.write('sweet');
    var div = goog.dom.createDom('div');
    goog.dom.$$('body')[0].appendChild(div);
    var editor = new goog.editor.Field(div);
    editor.cssStyles = 'html, body{height:100%;width:100%;margin:0;padding:0;font-family:Monaco;font-size:14px;}';
    editor.makeEditable();
    editor.focusAndPlaceCursorAtStart();
}