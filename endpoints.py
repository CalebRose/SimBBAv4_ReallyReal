import requests

# url = "https://simnba.azurewebsites.net/api/"
url = "http://localhost:8081/api/"

def GetMatchesForSimulation():
    res = requests.get(url + "simbba/matches/simulation")
    if res.status_code == 200:
        return res.json()
    return False


# Expected dictionary format for testing purposes
# {
#     "TestMatches": [
#         {
#             "HomeTeam": "IDHO",
#             "AwayTeam": "SMC",
#             "is_neutral": True
#         },
#         ...
#     ]
# }

# For testing purposes
def GetTestMatchesForSimulation(dto):
    res = requests.post(url + "admin/test/matches", json=dto)
    if res.status_code == 200:
        return res.json()
    return False