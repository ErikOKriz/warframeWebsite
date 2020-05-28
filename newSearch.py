# first the helper functions, each of these will take a line form htmlTemp.txt
# as input, and pull out the valuable information I want, and return it.
# Each function should have the same format of output.

def warframe(line):
    #this is our final return value
    value = []

    # if the line does not describe relics, then it is a part name
    if not ("Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line):
        partName = line
        partName.strip()

        # the way the html is structured, each part is listed multiple times,
        # so when we hit a part for he second time, we will already have all the information we need
        if partName in parts:
            # dropFound == 2 indicates that we have all the info we want
            dropFound = 2
        else:
            parts.append(partName)
            partRelics.append([])

    # else means the line describes the relics to drop for the most recent
    # partName, or parts[-1]
    else:
        prev = 0
        for y in range(len(line)):
            # if y is the first character of a new relic, or if it's the last
            # character in the line, then put that relic in partRelics
            if line[y] == '\n' or line[y:y + 4] == "Lith" or line[y:y + 4] == "Meso" or line[y:y + 3] == "Neo" or line[
                                                                                                                  y:y + 3] == "Axi" and y != 0:
                # send the string to partsRelics
                relic = line[prev:y]
                if relic != '':
                    partRelics[-1].append(relic)
                prev = y
        relic = line[prev:]
        partRelics[-1].append(relic)
    return

def weapon(line):
    return

def relic1(line):
    return

def relic2(line):
    return






#This program is meant to be able to parse an html file from htmlTemp.txt
# it is supposed to be a multi-functional program that can parse the data
# from warframe, weapon, companion, relic, and mission type pages. It will
# do this it will accept a typecode, this code will let the program know
# what lines are right before important info on that kind of htlm page and
# what lines are right after, so the program knows when to start and stop
# parsing data. The data it returns should be in a consistant format,
# it should be a list within a list.

def newSearch(typeCode):
    #initialize the iterable lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #initialize start variables

    #"Drop Locations" is the key word for warframes and weapons
    # warframe is type 0, weapons are type 1, relics are type 2
    keywords = ["Drop Locations", "Drop Locations", "Component"]

    #the endword for warframe is the first part name, need to be replaced in line
    # retrieved is the final end word for relics, but it won't be the next word, found.
    # that would be Intact, then it will keep searching for Chances, then it will
    # record more data until its true endword, Retrieved is found.
    endwords = ["partName", "Relics", "Retrieved" ]

    #relics have 2 groups of info I want, so I have a word where I have to stop
    # recording info, but then start again after I find another word, and then
    # really stop after I find the real final word
    kGWords = ['','', "Chances"]
    endwords2 = ['','', "Intact"]

    #This is a list of functions which will deal with each type on a line by line basis
    lineFunction1 = [waframe, weapon, relic]

    #since there are 2 blocks of info I want from relic pages, I need a line by line
    # extraction function for both blocks
    lineFunction2 = ['','',relic2]

    #This will be the final object we return, may regret initializing it as a list.
    finalReturn = []

    #this will act as a holding pen for information to be formatted for finalReturn
    tempList = []

    #fileplace lets us know where in the file we are, 0 means we have not found
    # the keyword yet, 1 means we found it and need to call on type-specific line
    # parsers, and 4 means we need to break, 2 and 3 are reserved incase some types
    # have multiple keywords, where 2 means we are looking for the second keyword, and
    # 3 means we have found it and need to call more type-specific line parsers.
    # this would occur when an html file has 2 blocks of info I want
    filePlace = 0

    #main for loop
    # At the end of this loop, tempList will be a list of all words that are part of
    # the important information, need another for loop to go through tempList to
    # organize that info for finalReturn
    for line in lines:
        if filePlace == 0:
            if keywords[typeCode] in line:
                filePlace = 1
        elif filePlace == 1:
            if endwords[typeCode] in line:
                break
            elif endwords2[typeCode] in line:
                #The question mark indicates the break between one block of
                # useful data and another
                tempList.append('?')
                filePlace = 3

            #else means we are in the first of our important blocks of lines
            else:
                #value is just the return value of the helper function, should
                # always be of the same format
                value = lineFunction1[typeCode](line)
                #do something with value
                tempList.append(value)

        #if we have not broken by now, then we are searching for our second
        # important block of code
        elif filePlace == 2:
            if kGWords[typeCode] in line:
                filePlace = 3

        #This means we are in our second important block of code and we should
        # extract that data
        elif filePlace == 3:
            if endwords[typeCode] in line:
                break
            else:
                #value has to be a list, even if it is just one object in the list
                value = lineFunction2[typeCode](line)
                #do something with value
                tempList = tempList + value
    #for testing
    print(tempList)

    return finalReturn