from urlGenerator import urlCreator
from urlGenerator import relicUrl
from goFetch import goFetch
import dropSearch
from relicSearch import relicSearch

#this main function should lok at our primes wanted Doc and for each line
#       create a url for the item on that line
#       fetch that url's html file and write to to htmlTemp.txt
#       parse htmlTemp.txt using another, external function, Parse()
#       using the info from parse(), write an entry for our file onto our database in the correct format.
# once it does that for every line in primes wanted, it closes the files and our database should be ready

def main():
    #primes is the list of items we want
    primes = open('primes.txt', 'r')
    #this deletes database for a new one, keep old copies ;)
    database = open('database.txt', 'w')

    #each line in primes is a different number
    for line in primes:
        #use url generator to create the url to search
        # type returns and integer. 1 means weapon, 2 means warframe
        #   add more later
        url, typeCode = urlCreator(line.capitalize())

        #get the html of that url and store it ih htmlTemp.txt
        goFetch(url)

        #parse out the drop tables from the html
        dropTables = dropSearch.dropSearch(typeCode)

        #insert the drop tables into database.txt
        # FORMAT - most important lines as this txt has to play well with the website
        database.write("Item: " + line.capitalize())

        for x in dropTables:
            database.write("Component: " + '\n'.join(x))

        #make sure there's an extra line between items
        database.write('\n' + '\n')

    #cleanup for database construction
    primes.close()
    database.close()

    #start constructing the relic databse
    database = open("database.txt", 'r')
    relicBase = open('relicTables.txt', 'w')

    #create the set of relics we need to look up
    relics = set()
    for line in database:
        #if the line describes a relic, add it to the set, do not want multiples
        if "Lith" in line or "Meso" in line or "Neo" in line or "Axi" in line:
            relics.add(line)

    #create the relicBase.txt database of relics
    for line in relics:
        url = relicUrl(line)

        #put relic info in htmlTemp.txt
        goFetch(url)

        #parse html data
        relicTable = relicSearch()

        #write the relic name
        words = line.split()
        relicBase.write('* ' + words[0] + ' ' + words[1] + '\n')

        #write the drop table
        for x in relicTable[0]:
            relicBase.write('   ' + x + '\n')
        relicBase.write("Drops From: " + '\n')

        if type(relicTable[1][0]) == list:
            relicBase.write("-+ Unvaulted" + '\n')
        #write the drops from table
        for x in relicTable[1]:
            if type(x) == list:
                relicBase.write('  ' + x[0] + ' ' + x[1] + ':')
                for i in x[2]:
                    relicBase.write('\n' + '     ' + i[0] + ' ' + i[1])
                relicBase.write('\n')
            else:
                relicBase.write('-- Vaulted' + '\n')
        relicBase.write('\n')

    #final cleanup
    database.close()
    relicBase.close()

    #no return value, check database.txt and relicBase.txt for returned values

#might not need this line when finally implemented
main()