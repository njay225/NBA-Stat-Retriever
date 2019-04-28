import bs4
from get_page import get_page

def get_team_info(team_page):

    record_text = team_page.find('div', {'data-template':"Partials/Teams/Summary"}).find('p').text.strip()

    #Remove White space and "Record: "
    record_text = " ".join(record_text.split()).strip('Record: ')

    #Get wins by splitting text at -
    wins = record_text.split('-')[0]

    #Taking text after the first '-'
    record_text = record_text.split('-')[1]

    #Get losses by splitting text at ','
    losses = record_text.split(',')[0]

    #Get team logo source
    team_logo = team_page.find('img', {'class':'teamlogo'})

    team_logo_src = team_logo['src']

    #Get Roster
    roster_table = team_page.find('table', {'id':'roster'})

    roster_data = roster_table.findAll('td', {'data-stat':'player'})

    roster = []

    for player in roster_data:
        player_name = player.find('a').text

        link = player.find('a')['href']

        roster.append({'name':player_name, 'link':link})

    return [wins, losses, team_logo_src, roster]
