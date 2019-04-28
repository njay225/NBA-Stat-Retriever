import bs4
from get_page import get_page


def get_team_list(team_page):
    team_th = team_page.find('div', {'class':'standings_confs table_wrapper'}).findAll('th')

    teams = []

    for th in team_th:

        if(th.find('a') != None):
            team_name = th.find('a').text

            team_link = th.find('a')['href']

            teams.append({'team':team_name, 'link':team_link})

    return teams
