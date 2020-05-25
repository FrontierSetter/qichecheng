function pad(num, n) {
    var len = num.toString().length;
    while(len < n) {
        num = "0" + num;
        len++;
    }
    return num;
}

function sum(arr){
    var result = 0;
    for(var i = 0; i < arr.length; ++i){
        result += arr[i];
    }
    return result;
}