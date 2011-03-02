{% autoescape off %}
dojo.provide("{{class_name}}");
dojo.declare("{{class_name}}", null, {
    constructor: function(args){
        dojo.safeMixin(this, args);
    },
    {% for property in properties %}{{ property.name }}:{{ property.to_js }}{% if not forloop.last %},{% endif %}
{% endfor %}});
{% endautoescape %}
