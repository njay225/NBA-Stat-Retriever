import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

#This function retrieves the html for a given team page
def get_page(link):
    #Create the URL
    url = 'https://www.basketball-reference.com' + link

    #Open connection to webpage using url
    uClient = urlopen(url)

    #Read the HTML
    html = uClient.read()

    #Close connection webpage
    uClient.close()

    #Return the parsed HTML
    return soup(html, 'html.parser')
