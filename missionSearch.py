#this file does the same thing as dropSearch and relicSearch, but it parses
# mission type html info

# the list of missions that these functions needs to catch are as follows
# set(capture, defection, defense, disruption, Empyrean, excavation,
#       extermination, interception, mobile defence, onslaught, rush
#       sabotage, spy, survival, profit-taker Bounty, salvage, pursuit,


#The Capture function works for Capture missions
#The Defense function works for Defense missions
#The Exterminate function works for the exterminate,
# defection, excavation, Survival, Spy, Sabotage, rescue, and Interception pages
#the mobile defense function also works for infested salvage


#Note, if oyu modify the tier system in Capture, it could be repurposed
# to work for capture and exterminate

def Capture():

    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    #missionList will be our final return value. It will be
    # a list of tuples, where each tuple, x, will have 4 items
    # in it, x[0] will be the planet, x[1] will be the mission
    # name, x[2] will be the faction at the mission,  x[3]
    # will be the level range of the mission, and x[4] will be
    # the tier of the mission. This format should be consistent
    # across all mission types
    missionList = []

    for line in lines:
        if filePoint == 0:
            if "Tier" in line:
                filePoint = 1
        elif filePoint == 1:

            #exit clause, doesn't matter if there are multiples of
            # total in the file as this will only trigger on the
            # 'total' we want.
            if "total" in line:
                break

            #setting up place holder variables and iterable list
            tempList = []

            prev = 0
            #the last character in the line is the tier. As long as the tiers
            # never go into double digits this should be fine
            tier = line[-1]

            #we don't want the tier interfering with the level range, which
            # is right before the tier with no space
            line = line[:-1]

            listLine = list(line)

            #max word count is 4, since we already have the tier
            wordCount = 0

            for y in range(len(listLine)):
                #each word in the line is capitalized, we are
                # interested in the first three words. The
                # first word is the planet, the second word is
                # the  name of the mission(the place on the
                # planet), and the third word is the faction
                # (faction is less important but it's good
                # to have the info). Next is the level range,
                # which is not as important. And the final character
                # this is not ' ' or '\n' is the tier of the
                # mission, very important

                if listLine[y] == ' ' and wordCount <= 3:
                    #this means when we run into "Orokin Derelict in the
                    # html, we won't think of it as two words.
                    listLine[y+1] = 'd'

                #So we don't append empty strings
                if prev != y:
                    if listLine[y].isupper() or listLine[y].isdigit() and wordCount < 3:
                        #this if statement could be more efficient
                        tempList.append(line[prev:y].strip())
                        prev = y
                        wordCount += 1
            #append what's left in the line, which is the mission level range
            tempList.append(line[prev:])

            #append the tier
            tempList.append(tier)

            #append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))


    #for testing
    #print(missionList)

    return missionList

#for testing
#Capture()

def Defense():
    #Note: each one of these functions should have the same beginning.
    # It's all about what words come before important lines in the file
    # and how to deal with the data.
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    #missionList will be our final return value. It will be
    # a list of tuples, where each tuple, x, will have 4 items
    # in it, x[0] will be the planet, x[1] will be the mission
    # name, x[2] will be the faction at the mission,  x[3]
    # will be the level range of the mission, and x[4] will be
    # the tier of the mission. This format should be consistent
    # across all mission types
    missionList = []

    #need these outside the loop as not all info for a mission
    # is on one line
    wordCount = 0
    tempList = []

    for line in lines:
        if filePoint == 0:
            if "Tier" in line:
                filePoint = 1
        elif filePoint == 1:
            if "total" in line:
                filePoint = 2
                continue

            #else is implied here
            if wordCount != 4:
                tempList.append(line.strip())
            wordCount += 1

            if wordCount == 6:
                wordCount = 0
                missionList.append(tuple(tempList))
                tempList = []

        #time to search for the dark sector section
        elif filePoint == 2:
            if "Tier" in line:
                filePoint = 3

        elif filePoint == 3:
            #exit clause, doesn't matter if there are multiples of
            # total in the file as this will only trigger on the
            # 'total' we want.
            if "total" in line:
                break

            #setting up place holder variables and iterable list
            tempList = []

            prev = 0
            #the last character in the line is the tier. As long as the tiers
            # never go into double digits this should be fine
            tier = line[-11:]


            #we don't want the tier interfering with the level range, which
            # is right before the tier with no space
            line = line[:-11]

            listLine = list(line)

            #max word count is 4, since we already have the tier
            wordCount = 0

            for y in range(len(listLine)):
                #each word in the line is capitalized, we are
                # interested in the first three words. The
                # first word is the planet, the second word is
                # the  name of the mission(the place on the
                # planet), and the third word is the faction
                # (faction is less important but it's good
                # to have the info). Next is the level range,
                # which is not as important. And the final character
                # this is not ' ' or '\n' is the tier of the
                # mission, very important

                if listLine[y] == ' ' and wordCount <= 3:
                    #this means when we run into "Orokin Derelict in the
                    # html, we won't think of it as two words.
                    listLine[y+1] = 'd'

                #So we don't append empty strings
                if prev != y:
                    if listLine[y].isupper() or listLine[y].isdigit() and wordCount < 3:
                        #this if statement could be more efficient
                        tempList.append(line[prev:y].strip())
                        prev = y
                        wordCount += 1
            #append what's left in the line, which is the mission level range
            tempList.append(line[prev:])

            #append the tier
            tempList.append(tier)

            #append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))

    #testing
    #print(missionList)

    return missionList

#test
#Defense()

#also works for Defection, Excavation, Spy, sabotage, rescue
# and Interception
def Exterminate():
    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    #missionList will be our final return value. It will be
    # a list of tuples, where each tuple, x, will have 4 items
    # in it, x[0] will be the planet, x[1] will be the mission
    # name, x[2] will be the faction at the mission,  x[3]
    # will be the level range of the mission, and x[4] will be
    # the tier of the mission. This format should be consistent
    # across all mission types
    missionList = []

    for line in lines:
        if filePoint == 0:
            if "Tier" in line:
                filePoint = 1
        elif filePoint == 1:

            #exit clause, doesn't matter if there are multiples of
            # total in the file as this will only trigger on the
            # 'total' we want.
            if "total" in line:
                break

            #setting up place holder variables and iterable list
            tempList = []

            prev = 0

            listLine = list(line)

            #only the first digit found is important, that signifies the start of
            # the level range
            digFound = 0

            for y in range(len(listLine)):
                #each word in the line is capitalized, we are
                # interested in the first three words. The
                # first word is the planet, the second word is
                # the  name of the mission(the place on the
                # planet), and the third word is the faction
                # (faction is less important but it's good
                # to have the info). Next is the level range,
                # which is not as important. And the final character
                # this is not ' ' or '\n' is the tier of the
                # mission, very important

                if listLine[y] == ' ':
                    #all spaces in this section are two or more word parts of one item
                    # we wantbut since each word is capital, we change each letter after
                    # a space to a lower case d in order to show that it is part of the
                    # same section. since we change the letter in listLine, and not line
                    # this does not change our final output.
                    listLine[y+1] = 'd'


                #So we don't append empty strings
                if prev != y:
                    if listLine[y].isupper():
                        #this if statement could be more efficient
                        tempList.append(line[prev:y].strip())
                        prev = y
                    elif listLine[y].isdigit() and digFound == 0:
                        tempList.append(line[prev:y].strip())
                        prev = y
                        digFound = 1


            #append what's left in the line, which is the mission level range
            tempList.append(line[prev:])

            if tempList[-1][-1] == '-':
                tempList[-1] = tempList[-1][:-1]
                tempList.append('-')

            #possible that elif is a problem here
            elif "Tier" in tempList[-1]:
                tempList[-1] = tempList[-1][-1]

            #append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))

    return missionList

#testing
#print(Exterminate())

def Assassinaion():
    return

#also works for infested salvage
def mobileDefense():

    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    missionList = []

    for line in lines:
        if filePoint == 0:
            if "Level" in line:
                filePoint = 1
        elif filePoint == 1:

            #exit clause, doesn't matter if there are multiples of
            # total in the file as this will only trigger on the
            # 'total' we want.
            if "total" in line:
                break

            #setting up place holder variables and iterable list
            tempList = []

            prev = 0

            listLine = list(line)

            #only the first digit found is important, that signifies the start of
            # the level range
            digFound = 0

            for y in range(len(listLine)):

                if listLine[y] == ' ':
                    listLine[y+1] = 'd'

                #So we don't append empty strings
                if prev != y:
                    if listLine[y].isupper():
                        #this if statement could be more efficient
                        tempList.append(line[prev:y].strip())
                        prev = y
                    elif listLine[y].isdigit() and digFound == 0:
                        tempList.append(line[prev:y].strip())
                        prev = y
                        digFound = 1

            #append what's left in the line, which is the mission level range
            tempList.append(line[prev:])

            #since none of these missions have tiers
            tempList.append('-')

            #append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))

    return missionList

#print(mobileDefense())


#this function is almost equivalent to the exterminate function, it
# just also pulls the dark sector missions. also works for excavation
def Survival():

    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    Ds = 0

    missionList = []

    for line in lines:
        if filePoint == 0:
            if line == "Tier":
                filePoint = 1
        elif filePoint == 1:

            if "total" in line:
                filePoint = 0
                if Ds == 1:
                    break
                else:
                    Ds += 1
                continue

            #This is here because when the tier of a dark sector mission
            # is dar sector # with \ax0 instead of a space
            if Ds == 1:
                line = line.replace(u'\xa0', u' ')


            #setting up place holder variables and iterable list
            tempList = []

            prev = 0

            listLine = list(line)

            #only the first digit found is important, that signifies the start of
            # the level range
            digFound = 0

            for y in range(len(listLine)):

                if listLine[y] == ' ':
                    listLine[y+1] = 'd'

                #So we don't append empty strings
                if prev != y:
                    if listLine[y].isupper():
                        tempList.append(line[prev:y].strip())
                        prev = y
                    elif listLine[y].isdigit() and digFound == 0:
                        tempList.append(line[prev:y].strip())
                        prev = y
                        digFound = 1

            #append what's left in the line, which is the mission level range
            tempList.append(line[prev:])

            #testing
            print(tempList)

            if tempList[-1][-1] == '-':
                tempList[-1] = tempList[-1][:-1]
                tempList.append('-')

            #possible that elif is a problem here
            elif "Tier" in tempList[-1]:
                tempList[-1] = tempList[-1][-1]

            #append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))

    return missionList

#print(Survival())

def Disruption():
    # initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    # filePoint just helps to know where in the file we are
    filePoint = 0

    Ds = 0

    missionList = []

    for line in lines:
        if filePoint == 0:
            if "Level" in line:
                filePoint = 1
        elif filePoint == 1:
            if "total" in line:
                if Ds == 1:
                    break
                Ds += 1
                filePoint = 0
                continue

            tempList = []

            prev = 0

            listLine = list(line)

            digFound = 0

            for y in range(len(listLine)):

                if listLine[y] == ' ':
                    listLine[y + 1] = 'd'

                # So we don't append empty strings
                if prev != y:
                    if listLine[y].isupper():
                        # this if statement could be more efficient
                        tempList.append(line[prev:y].strip())
                        prev = y
                    elif listLine[y].isdigit() and digFound == 0:
                        tempList.append(line[prev:y].strip())
                        prev = y
                        digFound = 1

            # append what's left in the line, which is the mission level range
            tempList.append(line[prev:])

            # since none of these missions have tiers
            tempList.append('-')

            # append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))

    return missionList

#print(Disruption())


