import requests
import os
from dotenv import load_dotenv

'''
This module is a wrapper for the League of Legends API provided by Riot.
Not all API calls provided by Riot are implemented.
'''

load_dotenv()
token = os.getenv("RIOT_TOKEN")

def tournament(tournament_url):

    req = requests.get(tournament_url)
    soup = BeautifulSoup(req.text, "html.parser")

    return_string = ''

    participants_links = soup.select("size-1-of-4")

    for links in participants_links:

        print("--")
        return_string = return_string + '\n \n' + tournament_team(links.a.get('href'))

    return return_string


def tournament_team(team_url):

    team_url = team_url + "/info"
    req = requests.get(team_url)
    soup = BeautifulSoup(req.text, "html.parser")

    team_string = soup.find("div", class_="name").get_text()

    members_summoner_ids = soup.find_all("i", class_= "fa-gamepad")

    for summoner in members_summoner_ids:

        print("!!")
        req_summonerID = v4_summoners(summoner.get_text())
        summonerID = req_summonerID.json()['id']
        team_string = team_string + '\n' + summoner.get_text() + get_soloq_rank(summonerID)

    return team_string


def gameinfo(user_name):

    '''
    provides available information about a player that is currently in-game
    '''

    user_id = summoner(user_name)

    #checks if the function didnt return an error message (they all start with the, which the ID does not)
    if user_id[:3] != "The":    
        request_match = requests.get('https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/' + user_id + '?api_key=' + token)

        #user is in-game
        if request_match.status_code == 200: 
            match_info = request_match.json() #load match data
            blue_side = 'Blue Side: \n \n'
            red_side = 'Red Side: \n \n'    

            for summoners in match_info['participants']: #loop thru all players
                
                if summoners['teamId'] == 100:
                
                    blue_side = blue_side + '  ' + summoners['summonerName'] + '   ' + champion(summoners['championId']) + '   ' + soloq_rank(summoners['summonerId']) + ' \n'

                else:

                    red_side = red_side + '  ' + summoners['summonerName'] + '   ' + champion(summoners['championId']) + '   ' + soloq_rank(summoners['summonerId']) + ' \n'                    
        
            game_info = blue_side + '\n' + red_side

            return game_info
        
        else:

            return 'Your requested user is currently not in-game.'





def summoner(user_name):

    '''
    provides the User ID for a given user name
    '''

    request = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + user_name + '?api_key=' + token)
    
    if request.status_code == 200:
        return request.json()['id']
    
    elif request.status_code == 404:
        return 'The requested user does not exist.'

    else:
        return 'The servers of riot are boosted, just like your teammates. Try again later!'


def soloq_rank(user_id):

    '''
    returns a string in the format of: <Tier Division LP Wins-Loses>
    Example: GOLD II 68LP 46-43 
    '''

    request = requests.get('https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + user_id + '?api_key=' + token)
    
    json_file = request.json()

    if json_file == []:

        return 'Not ranked in yet.'

    for i in range (0, len(json_file)):

        if json_file[i]['queueType'] == 'RANKED_SOLO_5x5':

            return json_file[i]['tier'] + ' ' + json_file[i]['rank'] + ' ' + str(json_file[i]['leaguePoints']) +  'LP ' + str(json_file[i]['wins']) + '-' + str(json_file[i]['losses'])

    return 'Not ranked in yet.'


def champion(champion_ID):

    #get name of a champion when given its ID

    champion_ID = str(champion_ID)
    r = requests.get('https://raw.githubusercontent.com/ngryman/lol-champions/master/champions.json')

    for elem in r.json():

        if elem['key'] == champion_ID:
            return elem['name']
