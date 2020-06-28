from goFetch import goFetch
import json

#this program's function is to fetch all primes from the warframe wiki and sort them into a text file

#this function looks at the prime page of the warframe wiki and creates some arrays of the names of
# all the primes on the site
def primeParse():
    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    #Initialize return values
    #No need to separate between primary/secondary/melee for weapons
    frames = []
    weapons = []
    sentinals = []
    archwings = []
    returnList = [frames, weapons, sentinals, archwings]

    for line in lines:
        if filePoint == 0:
            #look for list of prime warframes
            if "WarframesEdit" in line:
                filePoint = 1

        elif filePoint == 1:
            if "PrimaryEdit" in line:
                filePoint = 2
                continue
            words = line.split()

            for x in range(len(words) - 1):
                #if the word is a prime frame name
                if "Prime" in words[x+1]:
                    frames.append(words[x])

        elif filePoint == 2:
            if "CompanionsEdit" in line:
                filePoint = 3
                continue
            #finds all non-warframe primes
            words = line.split()
            for x in range(len(words) - 1):
                if words[x - 1] == 'Dual' or words[x - 1] == 'Nami':
                    weapons.append(str(words[x-1] + ' ' + words[x].lower()))
                elif "Edit" not in words[x] and "Prime" in words[x+1] and "Aegis" not in words[x]:
                    weapons.append(words[x])

        elif filePoint == 3:
            if "Sentinel WeaponsEdit" in line:
                filePoint = 4
                continue
            prev = 0
            for x in range(len(line) - 1):
                if prev != x and line[x] == ' ' or line[x].isupper() and line[x-1] == ')':
                    word = line[prev:x]
                    prev = x
                    if 'Prime' not in word and 'Collar' not in word and '(V)' not in word:
                        sentinals.append(word)
            #this line removes prime because kavasa prime has prime in the middle of the word
            # also if it ever gets vaulted, need to get rid of the '(V)'
            #word = line[prev:].replace('(V)', '')
            #sentinals.append(word)

        #this section could parse the prime sentinal weapons, but since those weapons drop with
        # their respective sentinals, we don't need this info
        elif filePoint == 4:
            if "ArchwingsEdit" in line:
                filePoint = 5

        #parse prime archwings (only odanata for now)
        elif filePoint == 5:
            if "ExtractorsEdit" in line:
                break
            words = line.split()
            for x in words:
                if "Prime" not in x and '(' not in x:
                    archwings.append(x)

    #put here because it's too hard to parse out
    weapons.append("Silva & aegis")
    weapons.sort()

    return returnList


#This function takes the info from the last function and stores it in a text file in json format
def primeBaseMain():
    goFetch("https://warframe.fandom.com/wiki/Prime")
    primeList = primeParse()

    #initialize some json objects to add data to
    data = {}
    data['primes'] = []

    iDCount = 0

    types = ['warframe', 'weapon','sentinal', 'archwing']

    #this for loop will create a json ready object which is a list of all primes
    for x in range(len(primeList)):
        for y in range(len(primeList[x])):
            data['primes'].append({
                'name' : primeList[x][y],
                'type' : types[x],
                'ID':str(iDCount),
                "partNames" : [],
                "partDrops" : []
            })
            iDCount += 1

    #next we have to add the parts to partNames and relics to partDrops using relicTables.txt
    with open('relicTables.txt', 'r') as file:
        relicDict = json.load(file)

    #y in this case is a dict describing a relic, with properties
    #   'Tier' : (lith/meso, etc.)
    #   'name' : 'a1'/'c4'/etc.
    #   'drops' : (an array of arrays where each sub array, x, has length 3 and x[0] is the prime, x[1] is the part to that prime, and x[2] is the rarity that relic drops that part of that prime.
    #   'dropsFrom' : (an array of all types of missions which dorp that relic and the chances it drops form those missions, if ['dropsFrom'] == 0, then it is a vaulted relic
    #   'isBaro' : '1' or '0' based on whether or not it is a baro relic or not
    #   'ID' : (just an ID number to identify each relic)
    #this for loop will fill in partNames and partDrops for all primes
    for z in data['primes']:
        for y in relicDict['relics']:
            #if there are no more drops to look at, stop iterating with that object,
            # remove dict with no more drops
            if y["Drops"] == []:
                del y
                continue
            for x in y["Drops"]:
                #if the prime part this relic drops is a part the prime we are looking at in our z for loop
                if x[0] == 'Forma':
                    #we're never looking for formas
                    y['Drops'].remove(x)
                elif x[0] == z['name']:
                    #if the part is not already listed in partname, add it to partNames, and make a new partDrops list to hold drop info
                    if x[1] not in z['partNames']:
                        z['partNames'].append(x[1])
                        z['partDrops'].append([])
                    #need the index of the list we should put this drop info in
                    dropListIndex = z['partNames'].index(x[1])
                    #add the drop info to the partDrops section as shown in database.json
                    z['partDrops'][dropListIndex].append(str(y['Tier'] + ' ' + y['Name'] + ' ' +  x[2]))
                    #then remove x from the droptable as we've already seen it, this doesn't affect relicTables.txt, so this dict is disposible
                    y['Drops'].remove(x)


    #this will dump data in to primes.txt, which will make the text in primes a json ready object
    with open('primes.txt', 'w') as file:
        json.dump(data,file)


#test
#primeBaseMain()
