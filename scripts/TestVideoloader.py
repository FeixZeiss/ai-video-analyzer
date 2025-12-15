import YT.ChannelStorage as ChannelStorage
import YT.Videogetter as Videogetter

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import os
import json

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
if os.path.exists("YT/token/token.json"):
    credentials = Credentials.from_authorized_user_file("YT/token/token.json", scopes)
else:
    # Neue Authentifizierung starten
    flow = InstalledAppFlow.from_client_secrets_file("YT/token/client_secret.json", scopes)
    credentials = flow.run_local_server(port=0)

    # Token speichern für spätere Logins
    with open("token.json", "w") as token_file:
        token_file.write(credentials.to_json())

# YouTube-Service erstellen
youtube = build("youtube", "v3", credentials=credentials)

loader = ChannelStorage.ChannelStorage(youtube)
loader.add_Channel_By_Name("Fireship")

videogetter = Videogetter.Videogetter(loader.get_Channels(), youtube)
videogetter.get_Upload_IDs()
videoInformation = videogetter.getInformation()

# Öffnet die Datei im Schreibmodus ('w' = write)
with open("videos.json", "w", encoding="utf-8") as file:
    json.dump(videoInformation, file, ensure_ascii=False, indent=2)
