dojo.provide("tic.admin.shell.client.Shell");
dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
dojo.require("dojox.dtl");

dojo.declare("tic.admin.shell.client.Shell.History", null, {
    _history: [],
    _current : -1,
    _is_last: false,
    add: function(item){
        console.log("length: " + this._history.length);
        console.log("add: " + this._current);
        if(!dojo.trim(item)) return;
        this._history.push(item);
        this._is_last = true;
        this._current  = this._history.length;
    },
    clear: function(){
        this._history = [];
    },

    next: function(){
        this._is_last = false;
        console.log("length: " + this._history.length);
        console.log("next: " + this._current);
        if(this._current === -1) return ''
        if(this._current < this._history.length -1){
            this._current++;
        }
        return this._history[this._current];
    },
    prev: function(){
        this._is_last = false;
        console.log("length: " + this._history.length);
        console.log("prev: " + this._current);
        if(this._current === -1)return ''
        if(this._current > 0){
            this._current--;
        }
        return this._history[this._current];
    },
    currentIsLast: function(){
        return this._is_last;
    }
});

dojo.declare("tic.admin.shell.client.Shell",
    [dijit._Widget, dijit._Templated],
    {
        //        widgetsInTemplate: true,
        templateString: dojo.cache("tic.admin.shell.client", "resources/Shell.html"),
        _history: new tic.admin.shell.client.Shell.History(),
        focus: function(){
            console.log("fffff");
            this.input.focus();
        },
        submit: function(e){
            e.preventDefault();
            e.stopPropagation();
            console.log("sssss");
            var result = '';
            this._appendExecutedCommand(this.input.value, result);
            this._history.add(this.input.value);
            this.input.value = '';
            this.focus();
            this._scrollToBottom();

        },
        _appendExecutedCommand: function(command, result){
            command = dojo.trim(command);
            result = dojo.trim(result);
            var template = '';
            if (command.substr(-1) == ":") {
                template += '<div class="command">' + (this.input.value || '&nbsp;') + '</div>';
                template += '<div class="AdminShellPrompt">...&nbsp;</div>';
            } else {
                template += '<div class="command">' + (this.input.value || '&nbsp;') + '</div>';
                template += '<div>' + result + '</div>' +
                '<div class="AdminShellPrompt">&gt;&gt;&gt;&nbsp;</div>';
            }
            this.content.innerHTML += template;
        },
        _scrollToBottom: function(){
            this.rootContainer.scrollTop = this.rootContainer.scrollHeight
        },
        keydown: function(e){
            var keycode = e.keyCode;
            switch( keycode ) {

                case dojo.keys.TAB:
                    e.preventDefault();
                    console.log("tab");

                    break;

                // History Up
                case dojo.keys.UP_ARROW:
                    e.preventDefault();
                    if(dojo.trim(this.input.value) && this._history.currentIsLast())
                        this._history.add(this.input.value);
                    this.input.value = this._history.prev();
                    console.log("up");
                 
                    break;

                // History Down
                case dojo.keys.DOWN_ARROW:
                    e.preventDefault();
                    var v = this._history.next();
                    if(v)
                       this.input.value = v;
                    console.log("down");
                    break;

                default:
                    break;
            }
 
        }
    });