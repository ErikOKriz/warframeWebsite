#This program will take no input: this function will search
# through htmlTmp.txt, which contains the html information of a warframe wiki
# page and returns a drop table. This table is a list of tuples where item[0]
# is the item name, and item[1] is a list of all relics that drop, at what
# rarity, and whether the relic is vaulted or not

#info is different
def Frame():
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]

    #dropTable is going to be the final returned item, which will be used
    # by the main function as the info for database.txt
    dropTable = []

    #dropFound is how the program know where in the file it is
    dropFound = 0

    #partName is just initialized here, not totally necessary
    partName = ''

    #parts is a list of all the part names
    parts = []

    #part relics is a list of lists which contain the relics
    # that make up the parts of the parts list, in the format
    # of partRelics[x] is the list of all relics that can
    # roll parts[x].
    partRelics = []

    for line in lines:
        #line is a string

        #if you haven't found "drop locations" yet, keep going
        if dropFound == 0:
            if "Drop Locations" in line:
                #drop locations itself is not an interesting line, we want the
                # info that starts on the next line.
                dropFound = 1

        #dropFound == 1 only once we have found "Drop Locations" and before we exit
        elif dropFound == 1:

            #if the line does not describe relics, then it is a part name
            if not ("Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line):
                partName = line
                partName.strip()

                #the way the html is structured, each part is listed multiple times,
                # so when we hit a part for he second time, we will already have all the information we need
                if partName in parts:
                    #dropFound == 2 indicates that we have all the info we want
                    dropFound = 2
                else:
                    parts.append(partName)
                    partRelics.append([])

            #else means the line describes the relics to drop for the most recent
            # partName, or parts[-1]
            else:
                prev = 0
                for y in range(len(line)):
                    #if y is the first character of a new relic, or if it's the last
                    # character in the line, then put that relic in partRelics
                    if line[y] == '\n' or line[y:y+4] == "Lith" or line[y:y+4] == "Meso" or line[y:y+3] == "Neo" or line[y:y+3] == "Axi" and y != 0:
                        #send the string to partsRelics
                        relic = line[prev:y]
                        if relic != '':
                            partRelics[-1].append(relic)
                        prev = y
                relic = line[prev:]
                partRelics[-1].append(relic)


        #else only happens once we've gotten all the info we want from the txt
        # this is when dropFound == 2
        else:
            break
            #this builds the dropTable, format it so the website can read it easy

    for x in range(len(parts)):
        dropTable.append([parts[x]] + partRelics[x])
        dropTable[x][-1] = dropTable[x][-1] + '\n'

    file.close()

    #for testing
    #print(parts)
    #print(partRelics)
    #print(dropTable)

    return dropTable

#test
#Frame()

def weapon():
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]

    #dropTable is going to be the final returned item, which will be used
    # by the main function as the info for database.txt
    dropTable = []

    #dropFound is how the program knows where in the file it is
    dropFound = 0

    #partName is just initialized here, not totally necessary
    partName = ''

    #part relics is a list of lists which contain the relics
    # that make up the parts of the parts list, in the format
    # of partRelics[x] is the list of all relics that can
    # roll parts[x].
    partRelics = []

    for line in lines:
        #line is a string

        #if you haven't found "drop locations" yet, keep going
        if dropFound == 0:
            if "Drop Locations" in line:
                #drop locations itself is not an interesting line, we want the
                # info that starts on the next line.
                dropFound = 1

        #dropFound == 1 only once we have found "Drop Locations" and before we exit
        #the weapon pages
        elif dropFound == 1:
            if line[0:4] == "Lith":
                break
            partRelics.append([])
            prev = 0
            for y in range(len(line)):
                # if y is the first character of a new relic, or if it's the last
                # character in the line, then put that relic in partRelics
                if line[y] == '\n' or line[y:y + 4] == "Lith" or line[y:y + 4] == "Meso" or line[y:y + 3] == "Neo" or line[y:y + 3] == "Axi" and y != 0:
                    # send the string to partsRelics
                    relic = line[prev:y]
                    if relic != '':
                        partRelics[-1].append(relic)
                    prev = y
            relic = line[prev:]
            partRelics[-1].append(relic)
    # build dropTable
    for x in range(len(partRelics)):
        dropTable.append(partRelics[x])
        dropTable[x][-1] = dropTable[x][-1] + '\n'

    #testing
    #print(dropTable)
    #print(partRelics)

    return dropTable

def dropSearch(typeCode):
    if typeCode == 2:
        return Frame()
    elif typeCode == 1:
        return weapon()


