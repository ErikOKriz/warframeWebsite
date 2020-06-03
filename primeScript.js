//Define containers for use later
var primeList = document.getElementById("primeList");
    //Primes.json and its quantity
var primes;     
var primeCt;
    //Database.json and its quantity
var pTables;
var pTableCt;


/********* 
 * FUNCS *
 *********/

//Cookie G/S
/*
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
    document.cookie = name+'=; Max-Age=-99999999;';  
}
function displayCookie(cname) {
    alert(Cookies(cname));
}*/
function displayCookies() {
    var fname=getCookie("firstname");
    if (fname==null) {fname="";}
    if (fname!="") {fname="firstname="+fname;}
    var lname=getCookie("lastname");
    if (lname==null) {lname="";}
    if (lname!="") {lname="lastname="+lname;}
    alert (fname + " " + lname);
}
function getCookie(name) {
    var nameEQ = name + "=";
    //alert(document.cookie);
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1);
    if (c.indexOf(nameEQ) != -1) return c.substring(nameEQ.length,c.length);
    }
}

//Sidenav

function addTitleBar(title){
    primeList.insertAdjacentHTML('beforeend', `<h3>` + title + `</h3><hr>\n`);
}

//Main

function setFeaturedPrime(ID){
    //Find the prime in the primes list (NOT NECESSARY WHEN IDS ARE PROPERLY DONE)
    var tmp;
    for(var i = 0; i < pTableCt; i++){
        if(pTables[i].ID === ID){
            tmp = pTables[i];
            break;
        }
    }
    if(tmp == undefined){
        console.log("ERR: A prime was attempted to be set featured and failed (ID: " + ID + ")\n")
        return;
    }
    //Take the name insert _ for spaces if necessary
    var tag = name.replace(' ', '_');
    
    //Set Title and Type
    document.getElementById('itemName').innerHTML = tmp.name;
    document.getElementById('itemType').innerHTML = tmp.type;

    //Set Droptable
    document.getElementById('itemTable').innerHTML = null;
    for(var i = 0; i < 4; i++){
        var relicList = [tmp.parts.part0, tmp.parts.part1, tmp.parts.part2, tmp.parts.part3];
        if(i == 3 && relicList[3] == undefined) break;
        document.getElementById('itemTable').insertAdjacentHTML('beforeend','<tr>\n<th>' + tmp.partNames[i] + '</th>\n');
        var j = 0;
        while(relicList[i][j] != undefined)
            document.getElementById('itemTable').insertAdjacentHTML('beforeend','<td>' + relicList[i][j++] + '</td>\n');
    }
    document.getElementById('itemTable').insertAdjacentHTML('beforeend','</tr>\n');
    
    //Set wishlist tickbox. If cookied, display checked. Otherwise, display empty.
    if(getCookie(tag) != ""){
        document.getElementById('wishDiv').innerHTML = 
        `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:delWishlist('` + tag + `');" checked></p>`;
    }
    else{
        document.getElementById('wishDiv').innerHTML = 
        `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:addWishlist('` + tag + `');"></p>`;

    }
}
function addPrime(tmp){
    var string = `<a href="#" id="` + tmp.ID + `"onclick="javascript:setFeaturedPrime('` + tmp.ID + `')">` + tmp.name + `</a>\n`;
    primeList.insertAdjacentHTML('beforeend', string);
}
function addWishlist(name){
    //Cookies(name, name, 365);
    Cookies("Chroma","Yes", 365);
    displayCookie("Chroma");
    
}
function delWishlist(name){
    Cookies(name, "", 0);
    displayCookie(name);
}

/**********
 * SCRIPT *
 **********/

//Fetch primes.json and build primelist
var request = new XMLHttpRequest();
request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/Luca/erikScripts/primes2.txt');
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
var request2 = new XMLHttpRequest();
request2.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/Luca/erikScripts/database.json');
request2.onload = function(){
    pTables = JSON.parse(request2.responseText);
    pTableCt = pTables.length;
    console.log(pTables);

}
request2.send();



