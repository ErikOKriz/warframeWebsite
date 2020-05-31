var request = new XMLHttpRequest();
request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/Luca/primes.json');
request.onload = function(){
    var primeList = JSON.parse(request.responseText);
    //var primeList = request.responseText;
    console.log(primeList[0])
}
request.send();