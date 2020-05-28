#this file does the same thing as dropSearch and relicSearch, but it parses
# mission type html info

# the list of missions that this funciton needs to catch are as follows
# set(capture, defection, defense, disruption, Empyrean, excavation,
#       extermination, interception, mobile defence, onslaught, rush
#       sabotage, spy, survival, profit-taker Bounty, salvage, pursuit,
#

def missionSearch():

    #initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    #filePoint just helps to know where in the file we are
    filePoint = 0

    #missionList will be our final return value. It will be
    # a list of lists, where each list, x, will have 4 items
    # in it, x[0] will be the planet, x[1] will be the mission
    # name, x[2] will be the faction at the mission, and x[3]
    # will be the tier of the mission.
    missionList = []
    #try to make each element a fourple instead of a list, you're
    # not looking for them to change. can have 4 lists and make
    # tuples out of them in the end

    for line in lines:
        if filePoint == 0:
            if "Tier" in line:
                filePoint = 1
        elif filePoint == 1:

            #exit clause, doesn't matter if there are multiples of
            # total in the file as this will only trigger on the
            # 'total we want'.
            if "total" in line:
                break

            #setting up place holder variables and iterable list
            tempList = []
            prev = 0
            listLine = list(line)

            for y in range(len(listLine)):
                #each word in the line is capitalized, we are
                # interested in the first three words. The
                # first word is the planet, the second word is
                # the  name of the mission(the place on the
                # planet), and the third word is the faction
                # (faction is less important but it's good
                # to have the info). Next is the level range,
                # which doesn't matter. And the final character
                # this is not ' ' or '\n' is the tier of the
                # mission, very important

                #this will work for the first three words, need
                # a way to extract the tier

                if listLine[y] == ' ':
                    listLine[y+1] = 'd'

                if line[prev:y] is not '':
                    if listLine[y].isupper() or listLine[y].isdigit():
                        #this if statement could be more efficient
                        tempList.append(line[prev:y].strip())
                        prev = y

            #append a fourple to missionList of all pertinant info.
            missionList.append(tuple(tempList))


    #for testing
    print(missionList)

    return missionList


missionSearch()


