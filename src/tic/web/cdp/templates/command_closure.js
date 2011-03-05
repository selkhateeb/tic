{% autoescape off %}
goog.provide("{{class_name}}");
{% for type in types %}
goog.require('{{ type }}');{% endfor %}

{{class_name}} = function(args) {
    goog.mixin(this, args);
    {% for property in properties %}{% if property.closure_type %}{{ property.closure_type }}.apply(this.{{ property.name }}, args.{{ property.name }});{% endif %}{% endfor %}
};

{% for property in properties %}tic.web.cdp.cdp_tests.TCommand.prototype.{{ property.name }}={% if property.closure_type %}new {{ property.closure_type }}();{% else %}{{ property.to_js }};{% endif %}
{% endfor %}{% endautoescape %}
