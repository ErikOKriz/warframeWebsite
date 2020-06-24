from primeParser import primeBaseMain
from relicParse import relicParseMain
from FullSearch import fullSearchMain

#main function which reconstructs all databases if the need arises
def main():
    #need to do relic main first as the prime main pulls from the relic data
    relicParseMain()
    primeBaseMain()
    fullSearchMain()


#this function should only call itself for manuel testing. the goal is for another
# function to automatically call this when the database is out of date
#main()


