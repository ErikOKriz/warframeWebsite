#this function should be called on a relic by relic basis.
# we dont need to include the relic in the final output
# since we already knwo the relic

def relicSearch():
    #initialize file and lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #info starts after line that starts with Component.
    # compFOund helps us find broad places in the file,
    compFound = 0

    #each element in dropList is just an item that is dropped
    # by the relic. It's in order of rarity. with dropList[0,1, and 2]
    # being common drops. dropList[2,3] being uncommon drops, and
    # dropList[3] being the rare drop
    dropList = []

    #each element in missionList is a list, R,
    # where R[0] is the mission type, R[1] is the planet
    # or tier of that misison type that drops this relic
    # and R[2] is a list of tuples Q, where Q[0] is a
    # rotation (A,B, or C) and Q[1] is the percentage
    # chance that the relic drops from that mission on
    # Q[0]'s rotation
    missionList = []

    #relicTable is our final return value, just a list of
    # the relic's drop table and missions that it is dropped from
    relicTable = [dropList, missionList]

    #varibale to help sort out missions from html info
    missionCount = 0

    #dropCount serves the same purpose as missionCount, just in a separate part of the html
    # it also works with dropAdd to do this
    dropCount = 0

    #this list helps us choose which line to append when iterating through the drop tables
    # There's probably an easier way to do this
    dropAdd = [0, 3, 5, 7, 10, 12]

    #rotationList keeps track of mission rotations temporarily
    rotationList = []

    for line in lines:
        if compFound == 0:
            if "Component" in line:
                compFound = 1

        #Then the next line starts the drop table for the relic,
        # don't include percentages, they are always the same
        # for relic drops
        elif compFound == 1:
            #if the line does not describe a percentage or a ducat
            # amount, then it is a part drop
            if "Intact" in line:
                compFound = 2
            else:
                if dropCount in dropAdd:
                    dropList.append(line.strip())
                dropCount += 1

        #look for the start of mission drop list
        elif compFound == 2:
            #clause for vaulted relics
            if "Vaulted" in line:
                missionList.append("")
                break
            elif "Chances" in line:
                compFound = 3

        #when compFound == 3, we are in the mission dor list
        elif compFound == 3:
            #each mission drop table takes up 3 lines. each block
            # of lines is structured as such: Line 1: mission type
            # Line2: either the planet or of the mission type
            # Line3: list of rotation names (A,B, and-or C)
            # Line4: list of percentage chances.
            #       note: the percentage chances are correlated to
            #       rotation names. So the first rotation name
            #       listed has the first percentage chance to drop
            #       the relic and so on.
            # tier, can use these two lines
            # to get each specific mission it drops from

            #mission type
            if missionCount == 0:
                if "Retrieved" in line:
                    break
                else:
                    missionList.append([line.strip()])
                missionCount += 1

            #mission tier or planet
            elif missionCount == 1:
                missionList[-1].append(line.strip())
                missionCount += 1

            #rotation list
            elif missionCount == 2:
                rotationList = []
                listStr = list(line)
                for x in listStr:
                    if x is 'A' or x is 'B' or x is 'C':
                        rotationList.append(x)
                missionCount += 1

            #percentage list
            elif missionCount  == 3:
                listStr = list(line)
                perc = []
                prev = 0
                for y in range(len(listStr)):

                    if listStr[y] == ',':
                        perc.append(line[prev:y].strip())
                        prev = y + 1
                perc.append(line[prev:].strip())
                #now perc has all the percentages

                #after this loop, tempList will be a list of tuples
                # with the first element being A,B, or C and the second
                # element is the percentage odds that that mission at that
                # rotation will drop that relic.

                tempList = []
                for x in range(len(rotationList)):
                    tempList.append([rotationList[x], perc[x]])
                #the put the rotations/drop %s where they go
                missionList[-1].append(tempList)

                missionCount = 0

    return relicTable

