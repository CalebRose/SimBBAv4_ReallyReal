import requests
import json

url = "https://simnba.azurewebsites.net/api/"
# url = "http://localhost:8081/api/"

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

# Send match results to the API
def SendResults(dto):
    obj = json.dumps(dto, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    with open("last_import_payload.json", "w", encoding="utf-8") as f:
        f.write(obj)
    print(f"Posting import payload ({len(obj) / 1e6:.1f} MB)...")
    r = requests.post(url + "admin/results/import/", data=obj)
    print(f"Import response: HTTP {r.status_code} {r.text[:300]}")
    return r