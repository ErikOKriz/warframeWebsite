#taken from https://www.datacamp.com/community/tutorials/web-scraping-using-python

#this funciton should take a valid url as in input, and have no output.
# It should truncate htmlTemp.txt and place the html file of the url in
# htmlTemp.txt in text form.

from urllib3 import PoolManager
from bs4 import BeautifulSoup


def goFetch(url):
    http = PoolManager()
    #html is of a strange type, might be able to convery it to raw text
    html = http.request('GET', url)

    #the line below needs a second item to pass ot the function that
    # tells it how to parse the html data
    soup = BeautifulSoup(html.data)

    #can pull html title if wanted
    #title = soup.title

    #should be full html text of type string
    strText = soup.get_text()

    #edit text to get rid of white lines
    text = list(strText)
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

    strText = ''.join(text)

    print(strText)

    #next is to write text to htmlTemp.txt
    file = open('htmlTemp.txt', 'w')
    file.write(strText)

    file.close()


#test case
url1 = "https://warframe.fandom.com/wiki/Atlas/Prime"
goFetch(url1)