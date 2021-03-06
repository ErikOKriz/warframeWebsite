#taken from https://www.datacamp.com/community/tutorials/web-scraping-using-python

#this funciton should take a valid url as in input, and have no output.
# It should truncate htmlTemp.txt and place the html file of the url in
# htmlTemp.txt in text form. can easliy be changed to have an output/ go
# to another file

from urllib3 import PoolManager
from bs4 import BeautifulSoup



def goFetch(url):
    http = PoolManager()
    html = http.request('GET', url)

    #the line below needs a second item to pass ot the function that
    # tells it how to parse the html data
    #Can use the defualt python html parser (html.parser), xlml, or html5lib
    #   seems to be no difference between html.parser and xlml, html5lib, however
    #   pulls the raw htmml file instead of the text. will use parser for now
    #check https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    #for more info on this function.

    #this is the usual value
    soup = BeautifulSoup(html.data, "html.parser")

    #for testing
    #soup = BeautifulSoup(html.data, "html5lib")

    #tuns the htmp type of soup into a string
    strText = soup.get_text()

    #change string to list for in-place character replacement
    text = list(strText)

    #for loop to remove empty lines
    cur = 0
    for x in range(len(text)):
        if text[x] == '\n':
            if cur == 0:
                cur = x
            text[x] = ' '
        else:
            if cur != 0:
                cur = 0
                text[x-1] = '\n'
        if text[x] == '\xa0':
            text[x] = ' '

    #change list of chars back to string
    strText = ''.join(text)

    #next is to write text to htmlTemp.txt
    file = open('htmlTemp.txt', 'w')
    file.write(strText)
    file.close()


#test cases
#url1 = "https://warframe.fandom.com/wiki/Prime"
#url1 = "https://warframe.fandom.com/wiki/Void_Relic"
#url1 = "https://warframe.fandom.com/wiki/Module:Void/data?action=edit"
#url1 = "https://warframe.fandom.com/wiki/Mission"
#url1 = "https://warframe.fandom.com/wiki/Void_Relic?action=edit"
#url1 = "https://warframe.fandom.com/wiki/Module:Missions/data?action=edit"
#url1 = "https://warframe.fandom.com/wiki/Mercury"
#url1 = "https://n8k6e2y6.ssl.hwcdn.net/repos/hnfvc0o3jnfvc873njb03enrf56.html"
#url1 = "https://forums.warframe.com/forum/3-pc-update-notes"

#goFetch(url1)