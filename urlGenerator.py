# this program takes a string as input and creates a warframe wiki url based on that string.
# each string will be a line from our primes wanted text Doc.
# the format of the line should have each word of the item capitalized, and its type in lower
# case, example: Atlas Prime - warframe
# https://warframe.fandom.com/wiki/Soma_Prime
# https://warframe.fandom.com/wiki/Atlas/Prime

def urlCreator(line):
    sep = line.index('-')

    # item name is everything before the hyphen and type is everything after the hyphen
    itemName = line[:sep].strip()

    #this line is for any muli-word primes
    itemName = itemName.replace(' ', '_')
    type = line[sep + 1:].strip().lower()

    # on the warframe wiki, a prime warframe is a sub-page of the warframe ie. wiki.com/atlas/prime
    # while weapons occupy a totally different page ie. wiki.com/Tekko_Prime
    space = itemName.index(' ')
    if type == 'weapon':
        typeCode = 1
        itemName = itemName[:space] + '_' + itemName[space+1:].capitalize()
        url = "https://warframe.fandom.com/wiki/" + itemName
    elif type == 'warframe':
        typeCode = 0
        # warframes should only be split into two words, warframe name, and Prime.
        # This next line should make itemName just the warframe's name, because
        # we know 'Prime' comes after
        itemName = itemName[:space]
        url = "https://warframe.fandom.com/wiki/" + itemName + "/Prime"

    # can add more types, I'm just interested in weapons and warframes right now
    else:
        return "not a valid type"

    return url, typeCode

#this functions takes a line like "Meso B4 common"
# and return the url
# This function is only here to reduce clutter in the main function
def relicUrl(line):
    words = line.split()
    return "https://warframe.fandom.com/wiki/" + words[0] + '_' + words[1]