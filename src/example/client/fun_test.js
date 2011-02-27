
goog.require('example.client.fun');
goog.require('goog.testing.jsunit');

var conditions = [];
conditions[0] = 0;
conditions[1] = 0;
conditions[2] = 0;
conditions[3] = 0;
function testSweet(){
    st(1,2);
    st(0,2);
    st(0,4);
    for (i = 0; i < 4; i++) {
        console.log('condition[' + i + "]=" + conditions[i]);
    }

    console.log(i);
    assertTrue(true);
}

function st(a,b){
    if(function(){(a == 0)?conditions[0]++:conditions[1]++;return (a == 0);}() && function(){(b == 2)?conditions[2]++:conditions[3]++;return (b == 2);}() ){
        console.log('sweet');
    }
    
}