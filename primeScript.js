//Define containers for use later
var primeList = document.getElementById("primeList");
var primes;
var primeCt;

//Funcs
function setFeaturedPrime(name){
    var tmp;
    for(var i = 0; i < primeCt; i++){
        if(primes[i].name == name)
            tmp = primes[i];
    }
    document.getElementById('itemName').innerHTML = tmp.name;
    document.getElementById('itemType').innerHTML = tmp.type;
    document.getElementById('itemTable').innerHTML = null;
    for(var i = 0; i < 4; i++){
        document.getElementById('itemTable').insertAdjacentHTML('beforeend','<tr><th>' + tmp.partNames[i] + '</th>');
        document.getElementById('itemTable').insertAdjacentHTML('beforeend','<td>' + tmp.partDrops.part0[0] + '</td></tr>');
    }
}
function addPrime(tmp){
    //var string = `<a href="#" onclick="javascript:document.getElementById('itemName').innerHTML = '` + tmp.name + `'"> ` + tmp.name + `</a>\n`;
    var string = `<a href="#" onclick="javascript:setFeaturedPrime('` + tmp.name + `')">` + tmp.name + `</a>\n`;
    
    primeList.insertAdjacentHTML('beforeend', string);
}

function addTitleBar(title){
    primeList.insertAdjacentHTML('beforeend', `<h3>` + title + `</h3><hr>\n`);
}

//Fetch database.json
var request = new XMLHttpRequest();
request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/Luca/database.json');
request.onload = function(){
    primes = JSON.parse(request.responseText);
    primeCt = primes.length;
    console.log(primeCt);                           //Debug Print


    //Populate primelist with each prime
    addTitleBar("Frames");
    for(var i = 0; i < primeCt; i++){
        addPrime(primes[i]);
        addPrime(primes[i]);
        addPrime(primes[i]);
        addPrime(primes[i]);
        addPrime(primes[i]);
        addPrime(primes[i]);
        addPrime(primes[i]);


    }

};
request.send();



