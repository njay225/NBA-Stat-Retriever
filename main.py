#### IMPORTS ####
import bs4
from get_player_info import get_player_info
from get_team_info import get_team_info
from get_team_list import get_team_list
from get_page import get_page
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup as soup
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

session = FuturesSession()

#### SETTING GLOBAL VARIABLES ####
team_page = ''
team_info = ''
player_list = ''
players_dict = []
players = []
root = ''
chosen_team_name = ''

#### CREATE PLAYER CLASS ####
class Player:
    def __init__(self, name, games, points, rebounds, assists, field, three, free, effective, PER, WS, image):
        self.name = name
        self.games = games
        self.points = points
        self.rebounds = rebounds
        self.assists = assists
        self.field = field
        self.three = three
        self.free = free
        self.effective = effective
        self.PER = PER
        self.WS = WS
        self.image = image

#### THIS FUNCTION CHANGES THE CURRENT TEAM SELECTED AND LOADS ALL THE PLAYER
#### AND CALLS THE UPDATE UI FUNCTION ####
def change_team():
    global team_page, team_info, player_list, player_dict, players, chosen_team_name
    chosen_team_name = selected_team.get()

    for team in teams:
        if chosen_team_name == team['team']:
            chosen_team = team

    team_page = get_page(chosen_team['link'])

    team_info = get_team_info(team_page)

    #### GET PLAYER STATS FOR TEAM SELECTED ####
    player_list = team_info[3]

    players_dict = []

    for player in player_list:
        html = session.get('https://www.basketball-reference.com'+player['link'])

        players_dict.append({'name':player['name'], 'html':html.result()})

    players = []

    for player in players_dict:
        player_page = soup(player['html'].text, 'html.parser')

        player_info = get_player_info(player_page)

        players.append(Player(player['name'], *player_info))

    update_ui()

#### THIS FUNCTION UPDATES THE UI WITH THE CURRENT TEAM AND PLAYER INFORMATION ####
def update_ui():
    global root, team_info, players

    #### CREATING TOP LAYOUT ####
    top_frame = Frame(root, width=900, height=100)
    top_frame.grid(row = 0, column=0, pady=5)

    #### ADDING LOGO ####
    logo_frame = Frame(top_frame, width=100, height=100)
    logo_frame.grid(row = 0, column = 0, sticky="NSW")

    team_image_url = urlopen(team_info[2])
    raw_team_image_data = team_image_url.read()
    team_image_url.close()

    team_image = Image.open(BytesIO(raw_team_image_data))
    team_logo = ImageTk.PhotoImage(team_image)

    team_logo_label = Label(logo_frame, image=team_logo, borderwidth=1, relief="solid")
    team_logo_label.image = team_logo
    team_logo_label.grid(row=0, column=0, padx=10)

    #### ADDING TEAM INFO ####
    team_info_frame = Frame(top_frame, width=400, height=100)
    team_info_frame.grid(row = 0, column = 1, sticky = "N")

    team_name_label = ttk.Label(team_info_frame, text = chosen_team_name, font=(None, 23))
    team_name_label.grid(row = 0, column = 0, sticky="EW", padx=10, pady=10)

    wins_label = ttk.Label(team_info_frame, text = "Wins: " + team_info[0])
    wins_label.grid(row = 1, column = 0, sticky="EW", padx=10)

    losses_label = ttk.Label(team_info_frame, text = "Losses: " + team_info[1])
    losses_label.grid(row = 2, column = 0, sticky="EW", padx=10, pady=3)


    #### ADDING TEAM SELECTION ####
    team_selection_frame = Frame(top_frame, width = 400, height = 100)
    team_selection_frame.grid(row = 0, column = 2, sticky="NES")

    team_combobox = ttk.Combobox(team_selection_frame, textvariable=selected_team, state="readonly")
    team_combobox['values'] = team_name_list
    team_combobox.grid(row = 0, column = 0, pady=20, padx=200)

    confirm_button = Button(team_selection_frame, text="Change Team", command=change_team)
    confirm_button.grid(row=1, column=0, pady=5)

    #### ADDING PLAYER STATS ####
    bottom_frame = Frame(root)
    bottom_frame.grid(row = 1, column=0, columnspan=3, sticky="EW")

    player_canvas = Canvas(bottom_frame, width = 900, height = 600, scrollregion = (0,0,195*len(players),600))
    player_canvas.grid(row=0, column=0, sticky = "EW")
    player_canvas.grid_propagate(0)

    player_canvas_scroll = Scrollbar(bottom_frame, orient=HORIZONTAL, command=player_canvas.xview)
    player_canvas_scroll.grid(row=1, column=0, sticky='EW')

    player_canvas.configure(xscrollcommand=player_canvas_scroll.set)

    player_frames_holder = Frame(player_canvas)
    player_frames_holder.grid(row = 0)

    player_canvas.create_window(0,0, anchor="nw", height=600, width=10000*len(players), window=player_frames_holder)

    #### CREATING PLAYER FRAMES ####
    player_frames = []
    player_widgets = []

    for i in range(len(players)):
        player_frames.append(Frame(player_frames_holder, width = 175, height=525, borderwidth=1, relief="solid"))
        player_frames[i].grid(row = 0, column = i, sticky="NS", padx=10)
        player_frames[i].grid_propagate(0)

        player_widget_row = 0

        player_widgets.append({'name':ttk.Label(player_frames[i], text = players[i].name, font=(None, 15))})
        player_widgets[i]['name'].grid(row = 1, column= 0, pady=5, sticky="W")
        #player_widget_row += 1

        #### LOAD PLAYER IMAGE ####
        player_image_url = urlopen(players[i].image)
        raw_player_image_data = player_image_url.read()
        player_image_url.close()

        player_image = Image.open(BytesIO(raw_player_image_data))
        player_portrait = ImageTk.PhotoImage(player_image)

        player_widgets[i]['image'] = Label(player_frames[i], image=player_portrait, width=165)
        player_widgets[i]['image'].image = player_portrait
        player_widgets[i]['image'].grid(row = 0, column=0, pady=5, sticky="W")
        player_widget_row += 2


        player_widgets[i]['games'] = ttk.Label(player_frames[i], text = "Games: " + str(players[i].games))
        player_widgets[i]['games'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['points'] = ttk.Label(player_frames[i], text = "PPG: " + str(players[i].points))
        player_widgets[i]['points'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['rebounds'] = ttk.Label(player_frames[i], text = "RPG: " + str(players[i].rebounds))
        player_widgets[i]['rebounds'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['assists'] = ttk.Label(player_frames[i], text = "APG: " + str(players[i].assists))
        player_widgets[i]['assists'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['field'] = ttk.Label(player_frames[i], text = "FG%: " + str(players[i].field) + "%")
        player_widgets[i]['field'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['field'] = ttk.Label(player_frames[i], text = "3pt FG%: " + str(players[i].three) + "%")
        player_widgets[i]['field'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['field'] = ttk.Label(player_frames[i], text = "FT%: " + str(players[i].free) + "%")
        player_widgets[i]['field'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['field'] = ttk.Label(player_frames[i], text = "Effective FG%: " + str(players[i].effective) + "%")
        player_widgets[i]['field'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['field'] = ttk.Label(player_frames[i], text = "PER: " + str(players[i].PER))
        player_widgets[i]['field'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")
        player_widget_row += 1

        player_widgets[i]['field'] = ttk.Label(player_frames[i], text = "WS: " + str(players[i].WS))
        player_widgets[i]['field'].grid(row = player_widget_row, column= 0, pady=5, sticky="W")

#### GET THE LIST OF TEAMS ####
TEAM_LIST_PAGE = '/leagues/NBA_2019_standings.html'

teams = get_team_list(get_page(TEAM_LIST_PAGE))

team_name_list = []

for team in teams:
    team_name_list.append(team['team'])

#### CREATING UI ####
root = Tk()
root.title("Basketball Stats")
root.geometry("900x800")
root.resizable(width=FALSE, height=FALSE)

selected_team = StringVar()
selected_team.set(team_name_list[0])

change_team()

root.mainloop()
