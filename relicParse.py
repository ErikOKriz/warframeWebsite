from goFetch import goFetch
import json


#this function will read the void relic page on the wiki, it will read the info on
# each relic and create a master list of relic info. Finally, it will create a json
# file that contains all that info.
def relicParse():

    # initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    # filePoint just helps to know where in the file we are
    filePoint = 0

    #this will be our final return list, it'll be a list of objects described by
    # tempList
    relicList = []

    #list of all vaulted relics
    vaultedList = set()

    #this will be all the info about a relic. it will be a list containing the name of
    # the relic, the list of the drop table from the relic, with the first three listed
    # being the common drops, the next two being the uncommons, and the last one being
    # the rare. and finally a list of strings which describe which missions drop that
    # relic, at what rotation and at what percentage
    tempList = []

    for line in lines:
        #just dont want \xa0 in my file
        line = line.replace('\xa0', ' ')
        if filePoint == 0:
            if "Red text" in line:
                filePoint = 1

        elif filePoint == 1:
            #start inserting info into tempList
            if "Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line:
                tempList = [line, [], []]
                filePoint = 2

        elif filePoint == 2:
            tempList[1].append(line)
            if len(tempList[1]) == 6:
                filePoint = 3

        elif filePoint == 3:
            if "Chance" in line:
                filePoint = 4

        elif filePoint == 4:
            if "Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line:
                relicList.append(tempList)
                tempList = [line, [], []]
                filePoint = 2
                continue

            #final break
            elif "For information" in line:
                filePoint = 5
                continue

            #implied else

            #The rest of this goes on to construct tempList[2], which is a list of all
            # the missions the relic drops from and the chances of getting that relic
            listLine = list(line)

            prev = 0

            #this newline should become one object of tempList[2]. It will be have 4 elements:
            #  mission type, mission tier or planet, rotation drop, and percentage drop rate
            newLine = []

            #This should work for lines of the above format
            for y in range(len(listLine)):
                if prev != y and listLine[y].isupper() and listLine[y - 1] != ' ' and listLine[y - 1] != '-':
                    newLine.append(line[prev:y])
                    prev = y
            newLine.append(line[prev:prev + 1])
            newLine.append(line[prev + 1:])
            tempList[2].append(newLine)


        elif filePoint == 5:
            if "Axi" in line:
                filePoint = 6

        elif filePoint == 6:
            if "Baro" in line:
                break
            else:
                vaultedList.add(line)

    return relicList, vaultedList



def relicParseMain():
    #main relic page
    url = "https://warframe.fandom.com/wiki/Void_Relic"

    #put the relic page into htmlTemp.txt
    goFetch(url)

    #parse htmlTemp.txt
    RList, VList = relicParse()

    #now create the file relicBase.txt which holds all the information in json format
    data = {}
    data['relics'] = []

    iDCount = 0

    for y in range(len(RList)):

        if RList[y][0] in VList:
            data['relics'].append({
                'name':RList[0],
                'ID':str(iDCount),
                'drop table':tuple(RList[1]),
                'mission drops': "Vaulted, Nowhere"
            })
            iDCount += 1

        else:
            data['relics'].append({
                'name':RList[0],
                'ID':str(iDCount),
                'drop table':tuple(RList[1]),
                'mission drops':tuple(RList[2])
            })
            iDCount += 1

    with open('relicTables.txt', 'w') as file:
        json.dump(data, file)


