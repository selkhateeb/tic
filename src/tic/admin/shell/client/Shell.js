dojo.provide("tic.admin.shell.client.Shell");
dojo.require("tic.admin.shell.shared.ExecuteCommand");
dojo.require("tic.web.client.Service");
dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
dojo.require("dojox.dtl");
dojo.require("dojox.html.entities");

dojo.declare("tic.admin.shell.client.Shell.History", null, {

    /*
     * _history: (array)
     *      holds the statement history
     */
    _history: [],

    /*
     * _current: (integer)
     *      contains the index of the current history statement
     */
    _current : -1,
    
    /*
     * _resetted: (boolean)
     *      true when _current is reset
     */
    _resetted: false,

    /**
     * adds an item to the history
     *
     * Args:
     *      item: (string)
     *          the item we need to add
     */
    add: function(item){
        if(!dojo.trim(item)) return;
        this._history.push(item);

        //Reset the index and set the flag
        this._current  = this._history.length;
        this._resetted = true;
    },

    /**
     * clears the history and resets all states
     */
    clear: function(){
        this._history = [];
        this._current = -1;
        this._resetted = false;
    },

    /**
     * moves the current position to the next item and returns it
     *
     * Returns:
     *      a string containing the next item
     */
    next: function(){
        this._resetted = false;
        if(this._current === -1) return ''
        if(this._current < this._history.length -1){
            this._current++;
        }
        return this._history[this._current];
    },

    /**
     * moves the current position to the previous item and returns it
     *
     * Returns:
     *      a string containing the previous item
     */
    prev: function(){
        this._resetted = false;
        if(this._current === -1) return ''
        if(this._current > 0){
            this._current--;
        }
        return this._history[this._current];
    },

    /**
     * returns wheather _current points at the last item or not (ie resetted)
     */
    currentIsLast: function(){
        return this._resetted;
    }
});

dojo.declare("tic.admin.shell.client.Shell",
    [dijit._Widget, dijit._Templated],
    {
        _service: new tic.web.client.Service(),

        _inStatementBlock: false,

        /**
         * templateString:
         *      the main template for this widget
         */
        templateString: dojo.cache("tic.admin.shell.client", "resources/Shell.html"),

        /**
         * see dijit._Widget docs for more info
         */
        postCreate: function(){
            this.inherited(arguments);
            this.focus();
        },
        
        /**
         * _history:
         *      holds an instance of the history object
         */
        _history: new tic.admin.shell.client.Shell.History(),

        /**
         * places the cursor in the input box
         */
        focus: function(){
            this.input.focus();
        },

        _blockStatement: [],
        /**
         * executes the statement and displays the results
         */
        submit: function(e){
            //Cancel the default browser actions
            e.preventDefault();
            e.stopPropagation();
            var value = dojo.trim(this.input.value);
            if(!value && !this._inStatementBlock) {
                console.log('! value');
                this._appendExecutedStatement('', '');
                this._updateInput();
                return;
            }else if(!value && this._inStatementBlock){
                console.log('in statement');
                //execute
                dojo.forEach(this._blockStatement, function(statement) {
                    value += statement + '\n';
                });
                this._blockStatement = [];
                this._inStatementBlock = false;
                var result = '';
                this._service.execute(new tic.admin.shell.shared.ExecuteCommand({
                    statement: value
                }), this, function(result){
                    result = result.result;
                    this._appendExecutedStatement('', result);
                    this._updateInput();
                });
                return;
            }else if(this._isMultiLineStatement(value) || this._inStatementBlock){
                //in multiline block
                console.log('multi line');
                this._inStatementBlock = true;
                this._blockStatement.push(this.input.value);
                this._appendExecutedStatement(this.input.value, '');
                this._history.add(this.input.value);
                this._updateInput();
                return;
            }
            this._service.execute(new tic.admin.shell.shared.ExecuteCommand({
                statement: value
            }), this, function(json){
                result = json.result;
                this._appendExecutedStatement(value, result);
                this._history.add(value);
                this._updateInput();
            });
        },

        _isMultiLineStatement: function(statement){
            var last_char = statement.substr(-1);
            switch (last_char) {
                case ':':
                case '\\':
                    return true;
            }
            return false;
        },

        /**
         * appends the statement and its result to the display
         */
        _appendExecutedStatement: function(statement, result){
            statement = dojo.trim(statement)? statement: dojo.trim(statement);
            statement = statement.replace(/\s/g, '&nbsp;');
            result = dojox.html.entities.encode(result);
            console.log(result);
            var template = '';
            if (this._inStatementBlock) {
                console.log('in block');
                template += '<div class="statement">' + (statement || '&nbsp;') + '</div>';
                template += '<div class="AdminShellPrompt">...&nbsp;</div>';
            } else {
                template += '<div class="statement">' + (statement || '&nbsp;') + '</div>';
                template += '<div>' + result + '</div>' +
                '<div class="AdminShellPrompt">&gt;&gt;&gt;&nbsp;</div>';
            }
            this.content.innerHTML += template;
        },

        _updateInput: function(){
            //clear the input and focus and scroll to viewport
            this.input.value = '';
            this.focus();
            this._scrollToBottom();
        },

        /**
         * scroll to bottom of div
         */
        _scrollToBottom: function(){
            this.rootContainer.scrollTop = this.rootContainer.scrollHeight
        },

        /**
         * handles key down events
         */
        _keypress: function(e){
            var keycode = e.keyCode;
            switch( keycode ) {

                case dojo.keys.TAB:
                    //prevent tab so we dont lose focus
                    e.preventDefault();
                    break;

                // History Up
                case dojo.keys.UP_ARROW:
                    e.preventDefault();
                    if(dojo.trim(this.input.value) && this._history.currentIsLast()){
                        this._history.add(this.input.value);
                        //we need this since add resets the current index
                        this._history.prev();
                    }
                    this.input.value = this._history.prev();
                    break;

                // History Down
                case dojo.keys.DOWN_ARROW:
                    e.preventDefault();
                    var v = this._history.next();
                    if(v) this.input.value = v;
                    break;
            } 
        }
    });