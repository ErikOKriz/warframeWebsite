import requests


#this program takes a string as input and creates a warframe wiki url based on that string.
#each string will be a line from our primes wanted text Doc.
#the format oof the line should have each word of the item capitalized, and its type in lower
#case, example: Atlas Prime - warframe
#https://warframe.fandom.com/wiki/Soma_Prime
#https://warframe.fandom.com/wiki/Atlas/Prime
def urlCreator(line):
    sep = line.index('-')
    #item name is everything before the hyphen and type is everything after the hyphen
    itemName = line[:sep].strip()
    type = line[sep+1:].strip()
    # on the warframe wiki, a prime warframe is a sub-page of the warframe ie. wiki.com/atlas/prime
    # while weapons occupy a totally different page ie. wiki.com/Tekko_Prime
    space = itemName.index(' ')
    if type == 'weapon':
        itemName[space] = '_'
        url = "https://warframe.fandom.com/wiki/" + itemName
    elif type == 'warframe':
        #warframes should only be split into two words, warframe name, and Prime
        
        #this next line should make itemName just the warframe's name, because
        #we know 'Prime' comes after
        itemName = itemName[:space]
        url = "https://warframe.fandom.com/wiki/" + itemName + "/Prime"

    #can add more types, I'm just interested in weapons and warframes right now
    else:
        return "not a valid type"

    return url

#this program takes a url and retrieves the html file from that url, and stores it in text form
#in htmlTemp.txt, the file should be rewritten every time thsi program is run.
def goFetch(url):
    r = requests.get(url)
    with open('htmlTemp.txt', 'w') as file:
        file.write(r.text)
        file.close()

# this function should take htmlTemp as a raw html file, already in the directory
#   and parse out the data we want, we can either rewrite htmlTemp to hold this
#   pertinant data, or we could just return a list of that data and parse it out
#   in the main function.
def parse():
    return



#this main function should lok at our primes wanted Doc and for each line
#       create a url for the item on that line
#       fetch that url's html file and write to to htmlTemp.txt
#       parse htmlTemp.txt using another, external function, Parse()
#       using the info from parse(), write an entry for our file onto our database in the correct format.
def main():
