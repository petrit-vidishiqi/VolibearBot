import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOORNAMENT_TOKEN")

def upcoming_match_opponent(link, team):

    tournament_id = link.split("/")[5]

    print(tournament_id)

    request_upcoming=requests.get("https://api.toornament.com/viewer/v2/tournaments/" + tournament_id + "/matches?statuses=pending",
                 headers={"X-Api-Key":token, "Range":"matches=0-127"})

    upcoming_json = request_upcoming.json()

    for matches in upcoming_json:

        print("____________")
        print(matches)
        print("______________")
        print(type(matches))
        for data in matches["opponents"]:
            
            print(len(data))
            #if data["participant"]["name"] = team:
            continue   


    request_opponent = requests.get("https://api.toornament.com/viewer/v2/tournaments/3848209563225554944/participants/3961543106334777344",
                 headers={"X-Api-Key":token})


upcoming_match_opponent("https://www.toornament.com/en_US/tournaments/3848209563225554944/stages/", "Free Volibearlins Black")