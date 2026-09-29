url = "https://ncaa-api.henrygd.me/schedule-alt/basketball-men/d1/2026"

response = requests.get(url)
response.raise_for_status()
  

data = response.json()
