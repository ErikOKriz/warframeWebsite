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
                if "Edit" not in words[x] and "Prime" in words[x+1] and "Aegis" not in words[x]:
                    weapons.append(words[x])

        elif filePoint == 3:
            if "Sentinel WeaponsEdit" in line:
                filePoint = 4
                continue
            prev = 0
            for x in range(len(line) - 1):
                if prev != x and line[x].isupper() and line[x-1] != ' ' and line[x-1] != '(' or line[x+1] == '(':
                    word = line[prev:x]
                    prev = x
                    if '(V)' not in word:
                        sentinals.append(word.replace('Prime', ''))
            #this line removes prime because kavasa prime has prime in the middle of the word
            # also if it ever gets vaulted, need to get rid of the '(V)'
            word = line[prev:].replace('(V)', '').replace('Prime', '')
            sentinals.append(word)

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
    weapons.append("Silva_&_Aegis")

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
                'ID':str(iDCount)
            })
            iDCount += 1

    #next we have to add the parts to


    #this will dump data in to primes.txt, which will make the text in primes a json ready object
    with open('primes.txt', 'w') as file:
        json.dump(data,file)


#test
primeBaseMain()
