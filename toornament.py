import requests
import datetime
import os
from dotenv import load_dotenv
import riot

load_dotenv()
token = os.getenv("TOORNAMENT_TOKEN")

def upcoming_match_opponent(link, team):

    tournament_id = link.split("/")[5]

    print(tournament_id)

    request_upcoming=requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/matches?statuses=pending",
                 headers={"X-Api-Key":token, "Range":"matches=0-127"})

    upcoming_json = request_upcoming.json()


    found_match = False

    for matches in upcoming_json:
        
        try:
            if (matches["opponents"][1]["participant"]["name"] == team):

                try:
                    request_opponent = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants/" + matches["opponents"][0]["participant"]["id"],
                            headers={"X-Api-Key":token})
                    
                    return participant_roster(request_opponent)

                except TypeError:
                    print("uno")
                    return "Currently no upcoming opponent scheduled."
            
            elif (matches["opponents"][0]["participant"]["name"] == team):

                try:
                    print(matches["opponents"][1]["participant"]["name"])
                    request_opponent = requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/participants/" + matches["opponents"][1]["participant"]["id"],
                            headers={"X-Api-Key":token})
                    return participant_roster(request_opponent)

                except IndexError:
                    print("dos")
                    return "Currently no upcoming opponent scheduled."
        
        except TypeError:

            continue



def participant_roster(api_response):

    print("ehre")
    print("ehre")
    resp_json = api_response.json()
    op_gg = "https://euw.op.gg/multi/query="
    print(op_gg)

    ret = "Upcoming Opponent: " + resp_json["name"] + ' \n'
    ret = ret + "---------------------------------------------------" + ' \n'
    print(resp_json["lineup"])
    for players in resp_json["lineup"]:
        
        player = players["custom_fields"]["summoner_name"]
        print(player)
        ret = ret + player + " - " + riot.soloq_rank(riot.summoner(player)) + ' \n'
        op_gg = op_gg + player.replace(" ", "+") + "%2C"

    ret = ret + "---------------------------------------------------" + ' \n'
    ret = ret + "OP.GG Multisearch: " + ' \n' + ' \n'
    ret = ret + op_gg
    print(ret)

    return ret


def upcoming_matches(link, team):

    tournament_id = link.split("/")[5]

    print(tournament_id)

    request_upcoming=requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/matches?statuses=pending",
                 headers={"X-Api-Key":token, "Range":"matches=0-127"})

    upcoming_json = request_upcoming.json()

    print(upcoming_json)

    