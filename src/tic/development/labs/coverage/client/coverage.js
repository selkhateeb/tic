goog.provide('tic.coverage');

goog.require('tic');
goog.require('goog.dom');

tic.requireCss('tic.coverage.style');

/**
 * calculates and displays coverage information
 * @constructor
 */
tic.coverage = function(){
    
};

/**
 * calculates the coverage percentage
 */
tic.coverage.prototype.calculateCoveragePercentage = function(){
    var c = 0;
    for(var i=0; i< instrumentedObject.blockCounter; i++){
	if(!instrumentedObject.executedBlock[i]) {
	    instrumentedObject.executedBlock[i] = 0;
	    c++;
	}
    }
    return (instrumentedObject.blockCounter - c)/instrumentedObject.blockCounter * 100;
};

/**
 * renders the code with coverage
 */
tic.coverage.prototype.render = function(){
    var div = goog.dom.createDom('div');
    
    var executed = instrumentedObject.executedBlock;
    var commands = instrumentedObject.commands;
    var blockCounter = 0;
    console.log(executed);
    for(var i=1; i<commands.length; i++){ //start from 1 to skip the first 'undefined'
	var command = commands[i];
	if(this.adjustBlockNumber(command)) continue; // its a BEGIN or END of block don't care
	var executedBlockId = this.getCurrentBlock();
	var numberOfExecutions = executed[executedBlockId];
	var className = (numberOfExecutions == false) ? 'red' : 'green';
	var line = goog.dom.createDom('div', className);
	line.innerHTML = command.replace(/\s/g, '&nbsp; ');
	div.appendChild(line);
    }
    goog.dom.getDocument().body.appendChild(div);
};

/**
 * current block
 * @type {Number}
 */
tic.coverage.prototype.currentBlock_ = [];

/**
 * gets the block number for a command
 */
tic.coverage.prototype.adjustBlockNumber = function(command){
    var result = false;
    if (command.indexOf('BRT_BLOCK_BEGIN') != -1) {
        this.currentBlock_.push(Number(command.match(/BRT_BLOCK_BEGIN:(\d+)/)[1]));
	result = true;
    } else if(command.indexOf('BRT_BLOCK_END') != -1) {
	this.currentBlock_.pop();
	result= true;
    }
    return result;
};

/**
 * returns the top of currentBlock_
 */
tic.coverage.prototype.getCurrentBlock = function(){
    return this.currentBlock_[this.currentBlock_.length-1];
};
