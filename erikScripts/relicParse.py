from goFetch import goFetch
import json


#this function will read the void relic page on the wiki, it will read the info on
# each relic and create a master list of relic info. Finally, it will create a json
# file that contains all that info.
def relicParse():

    #place what we need in htmlTemp.txt
    goFetch("https://warframe.fandom.com/wiki/Void_Relic")

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
                tempList = [line, []]
                filePoint = 2

        elif filePoint == 2:
            if "Chance" in line:
                filePoint = 3

        elif filePoint == 3:
            if "Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line:
                relicList.append(tempList)
                tempList = [line, []]
                filePoint = 2
                continue

            elif "For information" in line:
                break
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
            tempList[1].append(newLine)

    return relicList

def VRelicParse():

    #place what we need in htmlTemp.txt
    goFetch("https://warframe.fandom.com/wiki/Module:Void/data?action=edit")

    # initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    # filePoint just helps to know where in the file we are
    filePoint = 0

    newLine = ''

    for line in lines:
        if filePoint == 0:
            if '"Relics"' in line:
                filePoint = 1
        elif filePoint == 1:
            if line.strip() == '}':
                break
            #implied else
            newLine = newLine + line

    #these replace effects are what turns our string into one that is accepted by json.loads(x)
    #can definately be made more efficient, but this works for now
    newLine = newLine.replace("Drops = { {", '"Drops" : [ [')
    newLine = newLine.replace('}}', ']]')
    newLine = newLine.replace(' = '," : ")
    newLine = newLine.replace("Tier", '"Tier"')
    newLine = newLine.replace("Name", '"Name"')
    newLine = newLine.replace("IsVaulted", '"IsVaulted"')
    newLine = newLine.replace('IsBaro', '"IsBaro"')
    newLine = newLine.replace('},{Item : ', '],[')
    newLine = newLine.replace('Item : ', '')
    newLine = newLine.replace('Part : ', '')
    newLine = newLine.replace('Rarity :', '')
    #this line gives us a good character to split the relic dicts by "?"
    newLine = newLine.replace('},{ "Tier"', '}?{"Tier"')

    #just to check what is getting output, for testing
    #with open('htmlTemp2.txt', 'w') as file:
        #file.write(newLine)

    relicDicts = []

    #each x at this point will be a dict in json format and cna be worked on.
    for x in newLine.split('?'):
        x = json.loads(x)
        relicDicts.append(x)

    #now have to take this relic Dicts, and use the dropsFrom tables from relicParse
    # in order to create a complete relic table

    MissionList = relicParse()
    for Y in relicDicts:
        Yname = str(Y["Tier"]) + ' ' + str(Y["Name"])
        for M in MissionList:
            #testing
            #print(str(Y["Tier"]) + ' ' + str(Y["Name"]))
            if M[0] == Yname:
                #if there is a mission which drops the relic, then it is not vaulted
                Y['DropsFrom'] = M[1]
                #once per missionList loop
                del Y['IsVaulted']
                MissionList.remove(M)
                #hopefully this just breaks the missionList loop
                break
        if 'DropsFrom' not in Y:
            Y["DropsFrom"] = '0'
            if "IsVaulted" in Y:
                del Y["IsVaulted"]
        if "IsBaro" not in Y:
            Y["IsBaro"] = 0

    #after this for loop, relicDicts should be modified in place enough for us
        #to make it the final return value

    return relicDicts

#test
#VRelicParse()



def relicParseMain():
    #create dictionary objects for all relics
    dataList = VRelicParse()
    #now create the file relicBase.txt which holds all the information in json format
    data = {}
    data['relics'] = []

    iDCount = 0

    for y in range(len(dataList)):
        #test
        dataList[y]["ID"] = iDCount
        data['relics'].append(dataList[y])
        iDCount += 1

    with open('relicTables.txt', 'w') as file:
        json.dump(data, file)


#for testing
#relicParseMain()
#VRelicParse()
#relicParse()

