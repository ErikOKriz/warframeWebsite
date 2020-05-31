var request = new XMLHttpRequest();
request.open('GET','file:///primes.json');
request.onload = function(){
    console.log(request.responseText);
}
request.send();