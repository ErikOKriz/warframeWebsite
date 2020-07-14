from goFetch import goFetch
import json


def FullSearch():

    #fetch the text file into htmlTemp, it's a very large file
    goFetch("https://n8k6e2y6.ssl.hwcdn.net/repos/hnfvc0o3jnfvc873njb03enrf56.html")

    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    filePoint = 0

    #this is for checking if the most recent word describes the start of
    # a new nodenode is in here
    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Phobos', 'Ceres', 'Sedna', 'Eris', 'Void', 'Derelict', 'Lua', 'Kuva_Fortress', 'Europa']

    commDrop = ['Common', 'Uncommon', 'Rare', 'Legendary', 'Ultra Rare', 'Very Common']

    #since this is a one line file, we don't need a for loop, just the first line
    line = lines[0]

    # this variable keeps track of the start of a new word
    prev = 0

    # this variable will keep track of the most recent word
    word = ''

    # This will be our final return value, it might be one of
    # many arrays we'll return, it will hold a series of
    # dictionaries which describe nodes on the starmap
    nodes = []

    # this is the temporary object to hold all the info of a node. It's
    # a dict to make it easier to input into a json file
    tempNode = dict()

    # this will describe one item dropping from a node
    tempDrop = []

    # this will describe all items dropped from a node, but then will
    # be trimmed to be just the relics the node drops
    nodeDrops = []

    #this list defines the words in the html we would like to ignore, most involving punctuation
    #skipWords = ['', '/', '(',')']

    # this is so we know the rarity of eahc drop
    rotation = ''

    #for debugging
    wordlist = []

    # this should be the main for loop
    for x in range(len(line)):
        # this statement should trigger when we are at the first character of a new word
        # needs to be long because there are a lot of different cases
        if line[x].isupper() and x > 0 and line[x - 1] != ' ' and line[x-1] != '-' or x > 0 and line[x].isdigit() and not line[
            x - 1].isdigit() and line[x-1] != '.' and line[x-1] != ',' and "Relic" not in line[x:x+7]:
            word = line[prev:x].replace('/','').replace(')', '').replace('(', '').replace('Event: ', '').strip()
            prev = x
            if "Rotation" in word:
                rotation = word.replace("Rotation ", '')
            #test
            #wordlist.append(word)
            #if word in skipWords:
                #continue

        # we only need to process beyond this when we come across a new word. Since we
        # iterate by character, each new character of a new word would have us process the
        # old word over and over again.
        else:
            continue

        # might not need this conditional, it might be enough to just check if the word is
        # in planets
        if filePoint == 0:
            if "Missions:" in word:
                filePoint = 1
                #test
                #wordlist = []

        # At this point, the file should be describing each mission node.
        # and we have to figure out what each word means. If the word is
        # a planet, then it's a new mission node, otherwise it's either
        # mission node info or the end of the node info.
        elif filePoint == 1:

            if word == "Veil":
                #Veil is the first thing after sanctuary onslaught and the
                # first thing we don't care about. Once we reach veil we've
                # seen all the nodes we care about
                break

            elif word in planets:
                # then it's a new node, and you need to create a new object
                # to hold the info as it comes
                #This if is here so we don't append an empty dict as we come across
                # the first planet name in the file
                if len(tempNode) > 0:
                    #before creating new node info, need to dump the old info into nodes
                    tempNode["RelicDrops"] = nodeDrops
                    nodes.append(tempNode)
                    nodeDrops = []
                tempNode = dict()
                tempNode["Planet"] = word
                rotation = ''

            #Else append the word to tempNode, use the len of tempNode to
            # determine what aspect of a node this word describes
            else:
                L = len(tempNode)
                #doesn't start at 0 because we have already added the planet
                if L == 1:
                    tempNode["Node"] = word
                elif L == 2:
                    tempNode["MissionType"] = word

                #in this case, it describes a drop
                elif L > 2:
                    if word in commDrop:
                        tempDrop.append(rotation)
                    else:
                        tempDrop.append(word)
                    if "%" in word:
                        if "Relic" in tempDrop[0]:
                            tempDrop[0] = tempDrop[0].replace(' Relic','')
                            nodeDrops.append(tempDrop)
                        tempDrop = []

    #testing
    #print(wordlist)

    #could pull more info from this file, but nodes is all we're after for right now
    return nodes


#this function take the output of the last function, and stores it in a text file
# in json format
def fullSearchMain():
    nodes = FullSearch()

    data = {}
    data["Nodes"] = []

    #This is so each node has an ID value
    iDCount = 0

    for y in range(len(nodes)):
        if nodes[y]["RelicDrops"] != []:
            nodes[y]["ID"] = str(iDCount)
            data["Nodes"].append(nodes[y])
            iDCount += 1


    with open("NodeBase.txt", 'w') as file:
        json.dump(data,file)


#testing
#fullSearchMain()