import json

with open("videos.json", "r", encoding="utf-8") as file:
    videoInformation = json.load(file)

print(f"{len(videoInformation)} Videos geladen.")
print(videoInformation[0]["title"])
