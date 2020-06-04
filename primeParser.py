from goFetch import goFetch
import json


#this program's function is to fetch all primes from the warframe wiki and sort them into a text file

def primeParse():
    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0
    frames = []
    #I don't think I need to separate between primary/secondary/melee for weapons
    weapons = []
    returnList = [frames, weapons]

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
                break

            words = line.split()


            for x in range(len(words) - 1):
                if "Edit" not in words[x] and "Prime" in words[x+1] and "Aegis" not in words[x]:
                    weapons.append(words[x])
    weapons.append("Silva & Aegis")


    return returnList






def primeBaseMain():
    goFetch("https://warframe.fandom.com/wiki/Prime")
    primeList = primeParse()

    #just to differentiate it from primes.txt
    primes = open('primes.txt', 'w')

    data = {}
    data['primes'] = []

    iDCount = 0

    for y in range(len(primeList[0])):
        data['primes'].append({
            'name': primeList[0][y],
            'type':'warframe',
            'ID': str(iDCount)
        })
        iDCount += 1
    for y in range(len(primeList[1])):
        data['primes'].append({
            'name':primeList[1][y],
            'type':'weapon',
            'ID':str(iDCount)
        })
        iDCount += 1

    with open('primes2.txt', 'w') as file:
        json.dump(data,file)



