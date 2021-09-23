import requests
import json

# https://gitlab.com/dword4/nhlapi/-/blob/master/stats-api.md

parameters = {
    "stats": "yearByYear"
    # Crosby: 8471675
}

response = requests.get("https://statsapi.web.nhl.com/api/v1/people/8471675/stats", params=parameters)

crosbyGoals = {}
crosbyYears = response.json()["stats"][0]["splits"]
for i in range(len(crosbyYears)):
    if crosbyYears[i]["league"]["name"] == "National Hockey League":
        year = crosbyYears[i]["season"][:4] + " " + crosbyYears[i]["season"][4:]
        goals = crosbyYears[i]["stat"]["goals"]
        if year in crosbyGoals.keys():
            crosbyGoals[year] = goals + crosbyGoals[year]
        else:
            crosbyGoals[year] = goals
print(crosbyGoals)
