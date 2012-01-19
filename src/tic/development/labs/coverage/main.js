
var fs = require('fs');
var instrumentation = require('./instrumentation.js');

fs.readFile(process.argv[2],'ascii', function(err, data){
    if(err) console.error('bad');
    var script = instrumentation.instrument(data, 0);
    console.log(script.instrumented);
    
   // console.log(script);
});
