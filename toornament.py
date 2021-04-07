import requests
import datetime
import os
from dotenv import load_dotenv
import riot
import pandas as pd

load_dotenv()
token = os.getenv("TOORNAMENT_TOKEN")

def standings(link, team):

    ret = "No groups available for this team."
    
    tournament_id = link.split("/")[5]

    requestGroups = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/groups",
                 headers={"X-Api-Key":token, "Range": "groups=0-49"})

    for groups in requestGroups.json():

        requestStages = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/stages/" + groups['stage_id'] + "/ranking-items?group_ids=" + groups['id'],
                 headers={"X-Api-Key":token, "Range": "items=0-49"})

        stages = requestStages.json()

        if stages != []:

            for groupMembers in stages:

                if groupMembers['participant']['name'] == team:

                    place = []
                    name = []
                    games = []
                    wins = []
                    draws = []
                    losses = []
                    points = []

                    for mem in stages:
                        
                        place.append(mem['position'])
                        name.append(mem['participant']['name'])
                        games.append(mem['properties']['played'])
                        wins.append(mem['properties']['wins'])
                        draws.append(mem['properties']['draws'])
                        losses.append(mem['properties']['losses'])
                        points.append(mem['points'])

                    d = {"Platz": place, "Teamname": name, "Spiele": games, "Siege": wins, "Unentschieden": draws, "Niederlagen": losses, "Punkte": points}
                    df = pd.DataFrame(d)
                    ret = "Powered by toornament.com \n \n" 
                    ret = ret + df.to_string(index=False)



    return ret


def upcoming_match_opponent(link, team):

    tournament_id = link.split("/")[5]

    print(tournament_id)

    request_upcoming=requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/matches?statuses=pending",
                 headers={"X-Api-Key":token, "Range":"matches=0-127"})

    upcoming_json = request_upcoming.json()

    found_match = False

    if upcoming_json == []:

        return "The tournament has finished."

    for matches in upcoming_json:
        
        try:
            if (matches["opponents"][1]["participant"]["name"] == team):

                try:
                    request_opponent = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants/" + matches["opponents"][0]["participant"]["id"],
                            headers={"X-Api-Key":token})
                    print(matches["opponents"][1]["participant"]["id"])
                    return participant_roster(request_opponent)

                except TypeError:
                    print("uno")
                    return "Currently no upcoming opponent scheduled."
            
            elif (matches["opponents"][0]["participant"]["name"] == team):

                try:
                    print(matches["opponents"][1]["participant"]["name"])
                    print(matches["opponents"][1]["participant"]["id"])
                    request_opponent = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants/" + matches["opponents"][1]["participant"]["id"],
                            headers={"X-Api-Key":token})
                    return participant_roster(request_opponent)

                except IndexError:
                    print("dos")
                    return "Currently no upcoming opponent scheduled."
        
        except TypeError:

            continue

    return "Currently no upcoming opponent scheduled."



def participant_roster(api_response):

    print("ehre")
    print("ehre")
    resp_json = api_response.json()
    op_gg = "https://euw.op.gg/multi/query="
    print(op_gg)

    ret = "Powered by toornament.com \n \n"
    ret = ret + "Upcoming Opponent: " + resp_json["name"] + ' \n'
    ret = ret + "---------------------------------------------------" + ' \n'
    ret = ret + roster_overview(api_response)

    return ret


def roster(link, team):


    tournament_id = link.split("/")[5]

    print(tournament_id)
    
    requestAmountParticipants=requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants",
                 headers={"X-Api-Key":token, "Range":"participants=0-49"})

    
    amountOfParticipants = int(requestAmountParticipants.headers['Content-Range'].split("/")[1])

    print(amountOfParticipants)
    for i in range (0, amountOfParticipants, 50):

        print(i, i+49)
        headerRange = "participants=" + str(i) + "-" + str(i + 49)

        requestParticipants=requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants",
                 headers={"X-Api-Key":token, "Range": headerRange})

        for participants in requestParticipants.json():

            if participants['name'] == team:

            
                requestRoster = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants/" + participants["id"],
                            headers={"X-Api-Key":token})

                ret = "Powered by toornament.com \n \n"
                ret = ret + "Requested Team: " + team + ' \n'
                ret = ret + "---------------------------------------------------" + ' \n'
                ret = ret + roster_overview(requestRoster)

                return ret 

    return "Provided Team name can not be found."

def roster_overview(api_response):

    ret = ""
    resp_json = api_response.json()
    op_gg = "https://euw.op.gg/multi/query="

    for players in resp_json["lineup"]:
        
        player = players["custom_fields"]["summoner_name"]
        print(player)
        ret = ret + player + " - " + riot.soloq_rank(riot.summoner(player)) + ' \n'
        op_gg = op_gg + player.replace(" ", "+") + "%2C"

    ret = ret + "---------------------------------------------------" + ' \n'
    ret = ret + "OP.GG Multisearch: " + ' \n' + ' \n'
    ret = ret + op_gg

    return ret
