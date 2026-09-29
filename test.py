score_url = f"https://ncaa-api.henrygd.me/game/6585386"

response = requests.get(url)
response.raise_for_status()
  

data = response.json()

print(data)
