//Define containers for use later
var primeList = document.getElementById("primeList");
var primes;
var primeCt;

//Funcs
function addPrime(tmp){
    primeList.insertAdjacentHTML('beforeend', `<p>` + tmp.name + `</p>\n`);
}

//Fetch database.json
var request = new XMLHttpRequest();
request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/Luca/database.json');
request.onload = function(){
    primes = JSON.parse(request.responseText);
    primeCt = primes.length;
    console.log(primeCt);                           //Debug Print

    //Populate primelist with each prime
    for(var i = 0; i < primeCt; i++){
        addPrime(primes[i]);
    }

};
request.send();



