{% autoescape off %}
goog.provide("{{class_name}}");
{{class_name}} = function(args) {
    goog.mixin(this, args);
};
{% for property in properties %}tic.web.cdp.cdp_tests.TCommand.prototype.{{ property.name }}={{ property.to_js }};
{% endfor %}
{% endautoescape %}
