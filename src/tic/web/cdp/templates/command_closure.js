{% autoescape off %}
goog.provide("{{class_name}}");
{{class_name}} = function(args) {
        goog.mixin(this, args);
        {{properties}}
};
{% endautoescape %}
