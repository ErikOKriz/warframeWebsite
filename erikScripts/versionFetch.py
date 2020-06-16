from goFetch import goFetch
from constructionMain import main

#this function should fetch the version number of warframe and store it as a json object in a text doc

def versionFetch():
    goFetch("https://forums.warframe.com/forum/3-pc-update-notes")

    # initialize the file and the lines
    file = open('htmlTemp.txt', 'r')
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    for line in lines:
        if "Hotfix" in line:
            version = line
            break

    words = version.split()

    file = open("version.txt")
    fileVersion = file.readline()
    file.close()

    if fileVersion != words[-1]:
        file = open("version.txt", 'w')
        file.write(words[-1])
        file.close()
        main()

#this is the function that should be called whenever someone accesses the site
# it should also be called last, after sending the info. the info will send
# quickly, but may be wrong, just need to refresh to solve that
#don't think I need to physically call this here. it should be called in js
#versionFetch()
