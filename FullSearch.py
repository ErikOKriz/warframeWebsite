from goFetch import goFetch



def FullSearch():

    #fetch into the text file, it's a very large file
    goFetch("https://n8k6e2y6.ssl.hwcdn.net/repos/hnfvc0o3jnfvc873njb03enrf56.html")

    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    filePoint = 0

    #This is for testing, to see if we're creating words when
    # we're supposed to.
    words = []

    #this is for checking if the most recent word describes the start of
    # a new nodenode is in here
    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Phobos', 'Ceres', 'Sedna', 'Eris', 'Void', 'Derelict', 'Lua', 'Kuva_Fortress', 'Europa']

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

    # this should be the main for loop
    for x in range(len(line)):
        # this statement should trigger when we are at the first character of a new word
        # needs to be long because there are a lot of different cases
        if line[x].isupper() and x > 0 and line[x - 1] != ' ' or x > 0 and line[x].isdigit() and not line[
            x - 1].isdigit() and line[x - 1] != '-' and line[x-1] != '.' and line[x-1] != ',' and "Relic" not in line[x:x+7]:
            word = line[prev:x].replace('/', '').replace(')', '').replace('(', '').strip()
            prev = x
            # words is for testing
            words.append(word)

        # we only need to process beyond this when we come across a new word. and since we
        # iterate by character, each new character of a new word would have us process the
        # old word over and over again.
        else:
            continue

        # might not need this conditional, it might be enough to just check if the word is
        # in planets
        if filePoint == 0:
            if word == "Missions:":
                filePoint = 1
                words = []

        # At this point, the file should be describing each mission node.
        # and we have to figure out what each word means. If the word is
        # a planet, then it's a new mission node, otherwise it's either
        # mission node info or the end of the node info.
        elif filePoint == 1:
            if word == "Veil":
                # or next filepoint, either way, veil is the first thing after
                # sanctuary onslaught and the first thing we don't care about.
                # Once we reach veil we've seen all important nodes
                # this will also have to stay at break in order to test that this works
                # to list all the nodes
                break

            elif word in planets:
                # then it's a new node, and you need to create a new object
                # to hold the info as it comes
                if len(tempNode) > 0:
                    nodes.append(tempNode)
                tempNode = dict()
                tempNode["Planet"] = word

            # else append the word to tempNode, use the len of tempNode to
            # determine what aspect of a node this word describes
            else:
                L = len(tempNode)
                if L == 0:
                    tempNode["Planet"] = word
                elif L == 1:
                    tempNode["Node"] = word
                elif L == 2:
                    tempNode["MissionType"] = word
                # else means the doc is describing drops for the node
                # drops consist of three words, probably don't need this
                # so don't go through the trouble of figuring it out. We
                # already know which relics drop from where.
                # else:
                # tempNode[""]

    #test
    print(nodes)
    print(words)

    #this is the return value for now, might need a more expansive list later
    return nodes


FullSearch()