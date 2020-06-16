from primeParser import primeBaseMain
from relicParse import relicParseMain
from FullSearch import fullSearchMain

#main function which reconstructs all databases if the need arises
def main():
    primeBaseMain()
    relicParseMain()
    fullSearchMain()


#this function should only call itself for manuel testing. the goal is for another
# function to automatically call this when the database is out of date
#main()


