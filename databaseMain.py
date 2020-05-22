from urlGenerator import urlCreator
from goFetch import goFetch
import dropSearch

#this main function should lok at our primes wanted Doc and for each line
#       create a url for the item on that line
#       fetch that url's html file and write to to htmlTemp.txt
#       parse htmlTemp.txt using another, external function, Parse()
#       using the info from parse(), write an entry for our file onto our database in the correct format.
# once it does that for every line in primes wanted, it closes the files and our database should be ready

def main():
    #primes is the list of items we want
    primes = open(primes.txt, 'r')
    #this deletes database for a new one, keep old copies ;)
    database = open(database.txt, 'w')

    #each line in primes is a different number
    for line in primes:
        #use url generator to create the url to search
        url, name = urlGenerator.urlCreator(line)
        #get the html of that url
        goFetch.goFetch(url)
        #parse out the drop tables from the html
        dropTables = Parser()
        #insert the drop tables into database.txt
    primes.close()
    database.close()
    return