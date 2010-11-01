dojo.provide("tic.client.form.ValidationTextarea");
dojo.require("dijit.form.Textarea");
dojo.require("dijit.form.SimpleTextarea");
dojo.require("dijit.form.ValidationTextBox");


dojo.declare(
    "tic.client.form.ValidationTextarea",
    [dijit.form.ValidationTextBox,dijit.form.Textarea],
    {
        invalidMessage: "This field is required",
        postCreate: function() {
            this.inherited(arguments);
        },

        validate: function() {
            var v = this.inherited(arguments);
            if (arguments.length==0)
                v = this.validate(true);
            return v;
        },

        validator: function(/*anything*/value, /*dijit.form.ValidationTextBox.__Constraints*/constraints){
            // Override base behavior of using a RegExp, it is unnecessarily complex and fails on multiple lines
            // contained in a Textarea.
            return !this._isEmpty(value);
        },

        _onInput: function() {
            this.inherited(arguments);
            // Validate as you type, means any widgets which depend on this get updated without user
            // having to click elsewhere to trigger onBlur.
            this.validate();
        },

        onFocus: function() {
            if (!this.isValid()) {
                this.displayMessage(this.getErrorMessage());
            }
        },

        onBlur: function() {
            // Force the popup of the invalidMessage.
            this.validate(false);
        }
    }
    );
dojo.declare(
    "tic.client.form.ValidationSimpleTextarea",
    [dijit.form.ValidationTextBox,dijit.form.SimpleTextarea],
    {
        invalidMessage: "This field is required",
        postCreate: function() {
            this.inherited(arguments);
        },

        validate: function() {
            var v = this.inherited(arguments);
            if (arguments.length==0)
                v = this.validate(true);
            return v;
        },

        validator: function(/*anything*/value, /*dijit.form.ValidationTextBox.__Constraints*/constraints){
            // Override base behavior of using a RegExp, it is unnecessarily complex and fails on multiple lines
            // contained in a Textarea.
            return !this._isEmpty(value);
        },

        _onInput: function() {
            this.inherited(arguments);
            // Validate as you type, means any widgets which depend on this get updated without user
            // having to click elsewhere to trigger onBlur.
            this.validate();
        },

        onFocus: function() {
            if (!this.isValid()) {
                this.displayMessage(this.getErrorMessage());
            }
        },

        onBlur: function() {
            // Force the popup of the invalidMessage.
            this.validate(false);
        }
    }
    );
