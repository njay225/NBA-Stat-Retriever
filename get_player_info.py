import bs4
from get_page import get_page

def get_player_info(player_page):

    #Retrieve Career Stats Div
    all_stats = player_page.find("div", {"class":"stats_pullout"})

    if all_stats != None:

        #Get Averages
        averages = all_stats.find('div', {"class":'p1'})

        average_stats = []

        for div in averages.findAll('div'):
            average_stats.append(div.find('p').text)

        #Get Percentages
        percentages = all_stats.find('div', {"class":'p2'})

        percentage_stats = []

        for div in percentages.findAll('div'):
            percentage_stats.append(div.find('p').text)

        #Get Advanced
        advanced = all_stats.find('div', {"class":'p3'})

        advanced_stats = []

        for div in advanced.findAll('div'):
            advanced_stats.append(div.find('p').text)

        player = average_stats + percentage_stats + advanced_stats
    else:
        player = [0,0,0,0,0,0,0,0,0,0]

    #Get image source
    player_image = player_page.find('img', {'itemscope':'image'})

    if player_image != None:
        player_image_src = player_image['src']
    else:
        player_image_src = 'https://d2cwpp38twqe55.cloudfront.net/req/201901023/images/players/scalabr01.jpg'

    player.append(str(player_image_src))

    return player
