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
//Wishlist structure generated from cookies
var wishlist;
var wishlistCt;
//ID of currently focused prime
var pFocusID;


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
    primeList.insertAdjacentHTML('beforeend', `<h3>` + title + `</h3><hr><hr>\n`);
}

//Main

function setFeaturedPrime(ID){
    //Find the prime tmp in the primes list
    var tmp = primes[ID];
    pFocusID = ID;
    if(tmp == undefined){
        console.log("ERR: A prime was attempted to be set featured and failed (ID: " + ID + ")\n")
        return;
    }
    //Take the name insert _ for spaces if necessary
    var tag = tmp.name.replace(' ', '_');

    //Remove the mid placeholder
    document.getElementById('itemPlaceholder').innerHTML = "";

    //Set Title
    document.getElementById('itemName').innerHTML = tmp.name;

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
    drawWishCheckbox();
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

    //Print Drop locations
    relicInfoHTML.insertAdjacentHTML('beforeend', "<h3>Drop Locations</h3>");
    if(relics[i].NodeDrops[0] == undefined){
        relicInfoHTML.insertAdjacentHTML('beforeend', `<p class="vaultErr">This relic is vaulted. :(</p>`);
    }
    else{
        /* Old method of printing mission type
        var j = 0;
        while(relics[i].DropsFrom[j] != undefined){
            var curr = relics[i].DropsFrom[j];
            relicInfoHTML.insertAdjacentHTML('beforeend', "<p>" + curr[1] + " " + curr[0] + "</p>");
            j++;
        }*/
        //For every NodeDrop location:
        for( var j = 0; relics[i].NodeDrops[j] != undefined; j++){
            var curr = relics[i].NodeDrops[j];
           
            //Print the planet, node, and mission type
            relicInfoHTML.insertAdjacentHTML('beforeend', "<h4>" + curr[1] + ", " + curr[0] + "<br>" + curr[2] + "</h4>");
            
            //Then print each drop within that node
            for( var k = 0; curr[3][k] != undefined; k++){
                //Save A, B, or C to rotation
                var rotation = curr[3][k][0][0];

                //Fill the drops in, depending on if it's rotation-based or not
                if(rotation != undefined)
                    relicInfoHTML.insertAdjacentHTML('beforeend', `<p class="chance">` + rotation + " - " + curr[3][k][1] +"</p>");
                else
                    relicInfoHTML.insertAdjacentHTML('beforeend', `<p class="chance">` + curr[3][k][1] +"</p>");
            }

            //Horizontal line to separate entries
            relicInfoHTML.insertAdjacentHTML('beforeend', "<hr>");
        }
    }
}
//Insert a formatted entry to the primes box on the far left
function addPrime(tmp){
    var string = `<a href="#" id="` + tmp.ID + `"onclick="javascript:setFeaturedPrime('` + tmp.ID + `')">` + tmp.name + `</a>`;
    primeList.insertAdjacentHTML('beforeend', string);
}
//Build the existing wishlist from cookies when the site opens
function genWishlist(){
    //Init the array and count
    wishlist = new Array(primeCt);
    wishlistCt = 0;
    
    //For each prime
    for(var i = 0; i < primeCt; i++){
        var tag = primes[i].name.replace(' ', '_');
        //If its cookie is set
        if(getCookie(tag) != null){
            //Insert the default struct for true, then set parts to true until there are no more. This leaves nonexistant parts with an undefined.
            wishlist[i] = {"name":tag, "wish":true, parts:[undefined, undefined, undefined, undefined]};
            //Check if any subpart cookies are set
            var partDataFound = false;
            for(var j = 0; primes[i].partNames[j] != undefined; j++){
                if(getCookie(wishlist[i].name + j) != null){
                    wishlist[i].parts[j] = true;
                    partDataFound = true;
                } 
                else
                    wishlist[i].parts[j] = false;
            }
            //Then set all to true if no data was found
            if(!partDataFound){
                for(var j = 0; wishlist[i].parts[j] != undefined; j++)
                    wishlist[i].parts[j] = true;
            }
            
            //Update the count and add the item to wishlist
            wishlistCt++;
            addWishlistItem(i);
        }else{
            wishlist[i] = {"name":tag, "wish":false, parts:[undefined, undefined, undefined, undefined]};
            //Assign false only to the parts that exist. Any nonexistent parts will be undefined
            for(var j = 0; primes[i].partNames[j] != undefined; j++)
                wishlist[i].parts[j] = false;
        }
    }
}
function drawWishCheckbox(){
    if(wishlist[pFocusID].wish == true){
        document.getElementById('wishDiv').innerHTML = 
            `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:delWishlist('` + pFocusID + `');" checked></p>`;
    }else{
        document.getElementById('wishDiv').innerHTML = 
            `<p>Add to Wishlist: <input type="checkbox" id="wishBox" onclick="javascript:addWishlist('` + pFocusID + `');"></p>`;
    }
}
//Add an item to the wishlist and handles all add events
function addWishlist(ID){
    setCookie(wishlist[ID].name, "wishedFor", 365);
    wishlist[ID].wish = true;
    addWishlistItem(ID);
    drawWishCheckbox();
    wishlistCt++;
}

//Remove an item from the wishlist and handles all delete events
function delWishlist(ID){
    eraseCookie(wishlist[ID].name);
    wishlist[ID].wish = false;
    for(var i = 0;  wishlist[ID].parts[i] != undefined; i++){
        wishlist[ID].parts[i] = false;
        eraseCookie(wishlist[ID].name + i);
    }
    drawWishCheckbox();
    delWishlistItem(ID);
    wishlistCt--;
}

//Insert a formatted entry to the wishlist box
function addWishlistItem(ID){
    var element = document.getElementById(wishlist[ID].name + '_wish');
    //If the relevant wish element is undefined, insert html for the name
    if(element == undefined){
        document.getElementById('wishTable').insertAdjacentHTML('beforeend', `
            <tr id="` + wishlist[ID].name + `_wish" class="wishPrime">
                <td><a href="#" onclick="javascript:delWishlist(` + ID + `)">x</a></td>
                <td><a href="#" onclick="javascript:setFeaturedPrime('` + ID + `')">` + wishlist[ID].name + ` Prime</a></td>
                <td id="` + wishlist[ID].name + `_wish_expander"><a href="#" onclick="javascript:expWishlistItem(` + ID + `)"><</a></td>
            </tr>`);
        //Then add a line for each part and do addWishlist
        for(var i = 0; wishlist[ID].parts[i] != undefined; i++){
            document.getElementById('wishTable').insertAdjacentHTML('beforeend', `
                <tr id="` + primes[ID].name + `_` + i + `_wish"></tr>`
            );
            if(wishlist[ID].parts[i] == true)
                addCheckedWishlistPart(ID, i);
            else
                addUncheckedWishlistPart(ID, i);
        }
        minWishlistItem(ID);
    }
    //Otherwise, it is hidden and needs to be displayed
    else{
        element.style.display = "table-row";
    }
}
//Minimize an item's entry in the wishlist box
function minWishlistItem(ID){
    for(var i = 0; document.getElementById(primes[ID].name + `_` + i + `_wish`) != undefined; i++)
        document.getElementById(primes[ID].name + `_` + i + `_wish`).style.display = "none";
    document.getElementById(wishlist[ID].name + `_wish_expander`).innerHTML = `<a href="javascript:expWishlistItem(` + ID + `)"><</a>`;
}
//Expand an item's entry in the wishlist box
function expWishlistItem(ID){
    for(var i = 0; document.getElementById(primes[ID].name + `_` + i + `_wish`) != undefined; i++)
        document.getElementById(primes[ID].name + `_` + i + `_wish`).style.display = "table-row";
    document.getElementById(wishlist[ID].name + `_wish_expander`).innerHTML = `<a href="javascript:minWishlistItem(` + ID + `)">v</a>`;
}
//Remove an entry from the wishlist box
function delWishlistItem(ID){
    minWishlistItem(ID);
    document.getElementById(wishlist[ID].name + '_wish').style.display = "none";
    console.log("Deleting wishlist item: " + wishlist[ID].name + '_wish');
}
//Subfunction for parts of primes
function addCheckedWishlistPart(ID, part){
    //console.log("Adding wishlist part " + ID + "," + part);       //DEBUG
    setCookie(wishlist[ID].name + part, "wishedFor", 365);
    wishlist[ID].parts[part] = true;
    var box = document.getElementById(primes[ID].name + `_` + part + `_wish`);
    if(box != undefined){
        box.innerHTML = (`
            <tr id="` + primes[ID].name + `_` + part + `_wish">
                <td><input type="checkbox" onclick="javascript:addUncheckedWishlistPart(` + ID + `,` + part + `);" checked></td>
                <td>`+ primes[ID].partNames[part] + `</td>
            </tr>`
        );
    }
}
//Subfunction for parts of primes
function addUncheckedWishlistPart(ID, part){
    //console.log("Removing wishlist part " + ID + "," + part);     //DEBUG
    eraseCookie(wishlist[ID].name + part);
    wishlist[ID].parts[part] = false;
    var box = document.getElementById(primes[ID].name + `_` + part + `_wish`);
    if(box != undefined){
        box.innerHTML = (`
        <tr id="` + primes[ID].name + `_` + part + `_wish">
            <td><input type="checkbox" onclick="javascript:addCheckedWishlistPart(` + ID + `,` + part + `);"></td>
            <td>`+ primes[ID].partNames[part] + `</td>
        </tr>`)
    }
}

function verFetch(){
    $.ajax({
        url: "erikScripts/versionFetch.py",
        success: function(response) {
            console.log("VerFetch called.");
        }
    });
}

/**********
 * SCRIPT *
 **********/

//Fetch primes.json and build primes
var request = new XMLHttpRequest();
//request.open('GET','erikScripts/primes.txt');
//request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/primes.txt');  //For local machine use.
request.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/innovation/erikScripts/primes.txt');  //For local machine use, innovation branch
request.onload = function(){
    primes = JSON.parse(request.responseText).primes;
    primeCt = primes.length;
    console.log(primes);                           //Debug Print

    //Generate the wishlist structure
    genWishlist();
    console.log(wishlist);

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
    addTitleBar("Companions");
    for(var i = 0; i < primeCt; i++){
        if(primes[i].type == "companion")
            addPrime(primes[i]);
    }
    addTitleBar("Archwings");
    for(var i = 0; i < primeCt; i++){
        if(primes[i].type == "archwing")
            addPrime(primes[i]);
    }
};
request.send();

//Fetch relicMasterTemp.txt and build pTables
var request3 = new XMLHttpRequest();
//request3.open('GET','erikScripts/relicTables.txt');
//request3.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/relicTables.txt'); //For local machine use.
request3.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/innovation/erikScripts/relicTables.txt'); //Innovation branch
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
//request4.open('GET','erikScripts/NodeBase.txt');
//request4.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/master/erikScripts/NodeBase.txt'); //For local machine use.
request4.open('GET','https://raw.githubusercontent.com/ErikOKriz/warframeWebsite/innovation/erikScripts/NodeBase.txt'); //For local machine use.
request4.onload = function(){
    nTables = JSON.parse(request4.responseText).Nodes;
    nTableCt = nTables.length;
    console.log(nTables);
}
request4.send();

