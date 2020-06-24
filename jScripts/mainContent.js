//Define containers for use later
var primeList = document.getElementById("primeList");
    //Primes.json and its quantity
var primes;     
var primeCt;
    //Database.json and its quantity
var pTables;
var pTableCt;
    //relicList.txt and qty
var relics;
var relicCt;
var relicEraIndex = Array(4);


/********* 
 * FUNCS *
 *********/

//Cookie G/S

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {   
    document.cookie = name+'=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';  
}
function displayCookie(cname) {
    alert(getCookie(cname));
}

//Sidenav

function addTitleBar(title){
    primeList.insertAdjacentHTML('beforeend', `<h3>` + title + `</h3><hr>\n`);
}

//Main

function setFeaturedPrime(ID){
    //Find the prime in the primes list
    var tmp = pTables[ID];
    if(tmp == undefined){
        console.log("ERR: A prime was attempted to be set featured and failed (ID: " + ID + ")\n")
        return;
    }
    //Take the name insert _ for spaces if necessary
    var tag = tmp.name.replace(' ', '_');

    //Remove the mid placeholder
    document.getElementById('itemPlaceholder').innerHTML = "";

    //Set Title and Type
    document.getElementById('itemName').innerHTML = tmp.name;
    document.getElementById('itemType').innerHTML = tmp.type;

    //Set Droptable
    var relicList = tmp.partDrops;
    document.getElementById('itemTable').innerHTML = null;
    for(var i = 0; relicList[i] != undefined; i++){
        document.getElementById('itemTable').insertAdjacentHTML('beforeend','<tr><th>' + tmp.partNames[i] + '</th>');
        for(var j = 0; relicList[i][j] != undefined; j++)
            document.getElementById('itemTable').insertAdjacentHTML('beforeend','<td><a href="#" onclick="javascript:setFeaturedRelic(`' + relicList[i][j] + '`)">' + relicList[i][j] + '</a></td>');
    }
    document.getElementById('itemTable').insertAdjacentHTML('beforeend','</tr>');
    
    //Set wishlist tickbox. If cookied, display checked. Otherwise, display empty.
    if(getCookie(tag) != null){
        document.getElementById('wishDiv').innerHTML = 
        `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:delWishlist('` + tag + `');" checked></p>`;
    }
    else{
        document.getElementById('wishDiv').innerHTML = 
        `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:addWishlist('` + tag + `');"></p>`;

    }
}
function setFeaturedRelic(droplocation){
    var dropsplit = droplocation.split(' ');
    var tier = dropsplit[0];
    var name = dropsplit[1];
    var i = 0;
    var end;
    
    //Skip to index that matches tier
    switch(tier){
        case "Lith": end =  relicEraIndex[1]; break;
        case "Meso": i = relicEraIndex[1]; end = relicEraIndex[2]; break;
        case "Neo": i = relicEraIndex[2]; end = relicEraIndex[3]; break;
        case "Axi": i = relicEraIndex[3]; end = relicCt; break;
    }
    
    //Find the matching name. If at any point tier != the correct one, 
    for(i; i < end; i++){
        if(relics[i].Name == name)
            break;
    }

    //Print Contents
    document.getElementById("relicTitle").innerHTML = relics[i].Tier + " " + relics[i].Name;
    var relicInfoHTML = document.getElementById("relicInfo");
    relicInfoHTML.innerHTML = "<h3>Contents</h3>";
    for(var j = 0; j < 6; j++){
        var str = relics[i].Drops[j][0];
        var tmpStr = relics[i].Drops[j][1];
        str += " " + tmpStr;
        var rarityStr;
        switch(j){
            case 0:
            case 1:
            case 2: rarityStr = '<p class="common">'; break;
            case 3:
            case 4: rarityStr = '<p class="uncommon">'; break;
            case 5: rarityStr = '<p class="rare">'; break;
        }
        relicInfoHTML.insertAdjacentHTML('beforeend',rarityStr +  str + "</p>");
    }

    //Print Drop location
    relicInfoHTML.insertAdjacentHTML('beforeend', "<h3>Drop Locations</h3>");
    if(relics[i].DropsFrom == "0"){
        relicInfoHTML.insertAdjacentHTML('beforeend', "<p>This relic is vaulted. :(</p>");
    }
    else{
        var j = 0;
        while(relics[i].DropsFrom[j] != undefined){
            var curr = relics[i].DropsFrom[j++];
            relicInfoHTML.insertAdjacentHTML('beforeend', "<p>" + curr[1] + " " + curr[0] + "</p>");
        }
    }


}
function addPrime(tmp){
    var string = `<a href="#" id="` + tmp.ID + `"onclick="javascript:setFeaturedPrime('` + tmp.ID + `')">` + tmp.name + `</a>`;
    primeList.insertAdjacentHTML('beforeend', string);
}
function addWishlist(name){
    setCookie(name, "asdf", 365);
    document.getElementById('wishDiv').innerHTML = 
        `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:delWishlist('` + name + `');" checked></p>`;
}
function delWishlist(name){
    eraseCookie(name);
    document.getElementById('wishDiv').innerHTML = 
        `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:addWishlist('` + name + `');"></p>`;
}
function verFetch(){
    $.ajax({
        url: "erikScripts/versionFetch.py",
        success: function(response) {
            console.log("VFetch called.");
        }
    });
}

/**********
 * SCRIPT *
 **********/

//Fetch primes.json and build primes
var request = new XMLHttpRequest();
request.open('GET','erikScripts/primes.txt');
//request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/primes.txt');  //For local machine use.
request.onload = function(){
    primes = JSON.parse(request.responseText).primes;
    primeCt = primes.length;
    console.log(primes);                           //Debug Print

    //Populate primelist with each prime
    addTitleBar("Frames");
    for(var i = 0; i < primeCt; i++){
        if(primes[i].type == "warframe")
            addPrime(primes[i]);
    }
    addTitleBar("Weapons");
    for(var i = 0; i < primeCt; i++){
        if(primes[i].type == "weapon")
            addPrime(primes[i]);
    }
};
request.send();

//Fetch database.json and build pTables
request2 = new XMLHttpRequest();
request.open('GET','erikScripts/database.json');
//request2.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/database.json');
request2.onload = function(){
    pTables = JSON.parse(request2.responseText);
    pTableCt = pTables.length;
    console.log(pTables);
}
request2.send();

//Fetch relicMasterTemp.txt and build pTables
var request3 = new XMLHttpRequest();
request.open('GET','erikScripts/relicTables.txt');
//request3.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/relicTables.txt');
request3.onload = function(){
    relics = JSON.parse(request3.responseText).relics;
    relicCt = relics.length;
    relicEraIndex[0] = 0;
    var i = 0;

    //Skip to the first meso, then store
    while(relics[i].Tier != "Meso" || relics[i] == undefined ) i++;
    relicEraIndex[1] = i;

    //Repeat for neo and axi
    while(relics[i].Tier != "Neo" || relics[i] == undefined ) i++;
    relicEraIndex[2] = i;
    while(relics[i].Tier != "Axi" || relics[i] == undefined ) i++;
    relicEraIndex[3] = i;
    console.log(relics);
}
request3.send();

//Fetch NodeBase.txt and build nTables
var request4 = new XMLHttpRequest();
request.open('GET','erikScripts/NodeBase.txt');
//request4.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/NodeBase.txt');
request4.onload = function(){
    nTables = JSON.parse(request4.responseText).Nodes;
    nTableCt = nTables.length;
    console.log(nTables);
}
request4.send();
