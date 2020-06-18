from goFetch import goFetch
from constructionMain import main

#this function should fetch the version number of warframe and store it as a json object in a text doc

def versionFetch():
    #this is the link I'm using for now, could probably find a better one
    goFetch("https://forums.warframe.com/forum/3-pc-update-notes")

    # initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    for line in lines:
        #we're only looking for one line in the file, the first one describing
        # a version of the game, which would be the latest version
        if "Hotfix" in line:
            version = line
            break

    words = version.split()

    file = open("version.txt", 'r')
    fileVersion = file.readline()
    file.close()

    #words[-1] is the last word in the line, which should be the version number
    #If the current version of the database does not match the latest version of
    # the game, then recreate the database
    if fileVersion != words[-1]:
        #write into version.txt the version of the game we're about to create a
        # database for
        file = open("version.txt", 'w')
        file.write(words[-1])
        file.close()
        #Recreate database using constructionMain.main()
        main()

#this is the function that should be called whenever someone accesses the site
# it should also be called last, after sending the html info. the info will send
# quickly, but may be wrong, just need to refresh to solve that
#versionFetch()
