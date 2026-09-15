url = f"https//:ncaa-api.henrygd.me/game/6595386/scoring-summary"

response = request.get(url)
response.raise_for_status()

score = response.json()

print(score)
