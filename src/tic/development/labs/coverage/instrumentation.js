// Copyright 2011 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Implements loading of external scripts, instrumentation
 * and generation of accessory script that helps to collect coverage.
 *
 * @author ekamenskaya@google.com (Ekaterina Kamenskaya)
 * @author serebryakov@google.com (Sergey Serebryakov)
 */

/**
 * Instruments content of script object given as parameter in such way:
 * for semantic block #i, it adds labels:
 * - "//BRT_BLOCK_BEGIN:i" for its begin;
 * - "//BRT_BLOCK_END:i" for its end;
 * - "scriptObjects[index].executedBlock[i] =
 *        (scriptObjects[index].executedBlock[i] ?
 *        scriptObjects[index].executedBlock[i] + 1 : 1);" after its beginning.
 * For example:
 * if (a == 0) {
 *   //BRT_BLOCK_BEGIN:12
 *   scriptObjects[2].executedBlock[12] = (scriptObjects[2].executedBlock[12] ?
 *       scriptObjects[2].executedBlock[12] + 1 : 1);
 *   b = 1;
 *   c = 2;
 *   //BRT_BLOCK_END:12
 * }
 * @param {Object} script Script object whose content should be instrumented.
 * @param {number} index Index of script object in scriptObjects array.
 * @return {Object} Script object with instrumented content.
 * @private
 */
var parseJS = require('./parse-js');
var gen = require('./process');

exports.instrument = function(scriptContent, index) {
  var script = new Object();
  // Dealing with <!-- strings.
  scriptContent = scriptContent.replace(/^\s*<\!--/, '');

  // parse() constructs the syntax tree by given JS code.
  // gen_code() generates the JS code by given syntax tree.
  scriptContent = gen.gen_code(parseJS.parse(scriptContent), true);
  var tokens = scriptContent.split('\n');
  var instrumentedContent = [
      'goog.global.instrumentedObject = {};\n',
      'goog.global.instrumentedObject.executedBlock = [];\n'
  ];//new goog.string.StringBuffer();

  // Counter of instructions in this script.
  var counter = 0;
  // Counter of blocks in this script.
  var blockCounter = 0;
  // Stack for numbers of blocks we are in.
  var blockStack = [];
  // Array containing escaped text of each instruction.
  var commands = [];

  for (var j = 0; j < tokens.length; j++) {
    var trimmedToken = tokens[j].replace(/^\s+|\s+$/g, ""); //goog.string.trim(tokens[j]);
    if (trimmedToken != '') {
      var concreteToken = tokens[j];
      var includeToAccessory = true;

      if (concreteToken.indexOf('%BRT_BLOCK_BEGIN%') != -1) {
        var blockNumber = ++blockCounter;
        blockStack.push(blockNumber);
        concreteToken = concreteToken.replace('%BRT_BLOCK_BEGIN%',
            '//BRT_BLOCK_BEGIN:' + blockNumber);
      } else if (concreteToken.indexOf('%BRT_BLOCK_COUNTER%') != -1) {
        var blockNumber = blockStack[blockStack.length - 1];
        /*concreteToken = concreteToken.replace('%BRT_SCRIPT_INDEX%', index).
          replace('%BRT_BLOCK_COUNTER%', blockNumber);*/
        concreteToken = concreteToken.replace(
            'window.scriptObjects[%BRT_SCRIPT_INDEX%].' +
            'executedBlock[%BRT_BLOCK_COUNTER%] = true',
            'goog.global.instrumentedObject.executedBlock[' + blockNumber +
            '] = (goog.global.instrumentedObject.executedBlock[' + blockNumber + 
	    '] ? goog.global.instrumentedObject.executedBlock[' + blockNumber + '] + 1 : 1)');
        includeToAccessory = false;
      } else if (concreteToken.indexOf('%BRT_BLOCK_END%') != -1) {
        var blockNumber = blockStack.pop();
        concreteToken = concreteToken.replace('%BRT_BLOCK_END%',
            '//BRT_BLOCK_END:' + blockNumber);
      }

      if (includeToAccessory) {
        commands[++counter] = escape(concreteToken);
      }

      // Prevent misinterpretation of "</script>" string as ending tag.
      //concreteToken = concreteToken.replace(/<\/script>/g, '<\\/script>');
      instrumentedContent.push(concreteToken);
      instrumentedContent.push('\n');
    }
  }
  instrumentedContent.push('goog.global.instrumentedObject.counter = ' + counter + ';\n');
//  instrumentedContent.push('goog.global.instrumentedObject.commands = [');
  
    for(var i = 0; i < commands.length; i++)
	commands[i] = '\n"' + unescape(commands[i]) + '"';
    instrumentedContent.push('goog.global.instrumentedObject.commands = [' + commands.join() + '];\n');
  script.instrumented = instrumentedContent.join('');//toString();
  script.counter = counter;
  script.commands = commands;
  script.blockCounter = blockCounter;
  return script;
};

