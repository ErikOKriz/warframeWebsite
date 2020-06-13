from goFetch import goFetch

#This function will look at all html pages for all the planets and record the data
# from each node on the planet. Since this info is being used to figure out if the
# node drops a certain relic, the relavant info is the mission type, the tier, the
# level, and the planet

def nodeParse():

    planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Phobos', 'Ceres', 'Sedna', 'Eris', 'Void', 'Derelict', 'Lua', 'Kuva_Fortress', 'Europa']

    #this will be our final return value, it will be a list of dictionaries. To be
    # turned to a json file
    nodeList = []


    for y in planets:
        #this sets the planet's html file into htmlTemp to grab later
        goFetch("https://warframe.fandom.com/wiki/" + y)

        # initialize the file and the lines
        file = open('htmlTemp.txt', 'r')
        lines = file.readlines()
        lines = [x.strip() for x in lines]
        file.close()

        filePoint = 0

        # this is a temporary storage place for a member of nodeList. It is a dicitonary
        # where all its keys are values listed aboce as important for relics, in addition
        # to the node's name.
        TempD = dict()

        for line in lines:
            if filePoint == 0:
                




