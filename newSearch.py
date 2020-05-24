#helper functions for Search()
def weapon2(line):
    dropLine = []

    if line[0:4] == "Lith":
        return ["Break"]
    prev = 0
    for y in range(len(line)):
        # if y is the first character of a new relic, or if it's the last
        # character in the line, then put that relic in partRelics
        if line[y] == '\n' or line[y:y + 4] == "Lith" or line[y:y + 4] == "Meso" or line[y:y + 3] == "Neo" or line[y:y + 3] == "Axi" and y != 0:
            # send the string to partsRelics
            relic = line[prev:y]
            if relic != '':
                dropLine.append(relic)
            prev = y
    relic = line[prev:]
    dropLine.append(relic)
    return dropLine

def warframe2(line):
    dropLine = []

    # if the line does not describe relics, then it is a part name
    if not ("Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line):
        partName = line
        partName.strip()
        dropLine.append(partName)
        return dropLine

    # else means the line describes the relics to drop for the most recent
    else:
        prev = 0
        for y in range(len(line)):
            # if y is the first character of a new relic, or if it's the last
            # character in the line, then put that relic in partRelics
            if line[y] == '\n' or line[y:y + 4] == "Lith" or line[y:y + 4] == "Meso" or line[y:y + 3] == "Neo" or line[y:y + 3] == "Axi" and y != 0:
                # send the string to partsRelics
                relic = line[prev:y]
                if relic != '':
                    dropLine.append(relic)
                prev = y
        relic = line[prev:]
        dropLine.append(relic)
        return dropLine



#this is a new dropSearch that has no repeated lines
def search(typeCode):
    file = open('htmlTemp.txt', 'r')
    lines = file.readline()
    lines = [x.strip() for x in lines]

    #dropFound is how the program knows where in the file we are
    dropFound = 0

    #this function will build the dropTable as it goes
    dropTable = []

    #if the item is a warframe (typeCode == 2), then part helps it
    # sort html info
    part = 0

    for line in lines:
        if dropFound == 0:
            if "Drop Locations" in line:
                dropFound = 1
        elif dropFound == 1:
            if typeCode == 1:
                dropLine = weapon2(line)
                if dropLine[0] == ["break"]:
                    break
                #otherwise it should return a complete line for
                # the droptable
                else:
                    dropTable.append(dropLine)
            elif typeCode == 2:
                #dropLine is a list with all info pulled from the line
                dropLine = warframe2(line)
                for x in dropTable:
                    if dropLine[0] == x[0]:
                        break
                #if part == 0, that means the last line
                if part == 0:
                    dropTable.append(dropLine)
                    part = 1
                #if the line does not describe a part, or break the loop
                # then it's a list of relics that builds the most recent
                # part
                elif part == 1:
                    dropTable[-1] = dropTable[-1] + dropLine

    #now build dropTable
    file.close()

    return dropTable
