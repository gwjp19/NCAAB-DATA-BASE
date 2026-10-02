score_url = f"https://localhost:3000/game/6595386"

response = requests.get(url)
response.raise_for_status()
  

data = response.json()

print(data)
