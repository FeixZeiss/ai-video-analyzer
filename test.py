from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Berechtigungen: Nur Lesezugriff auf YouTube-Daten
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# OAuth-Flow starten
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes)
credentials = flow.run_local_server(port=0)

# YouTube-Service mit OAuth-Zugang
youtube = build("youtube", "v3", credentials=credentials)

# Beispielanfrage: Suche nach Videos
request = youtube.search().list(
    q="Python Tutorial",
    part="snippet",
    maxResults=5
)
response = request.execute()

# Ergebnisse ausgeben
for item in response["items"]:
    print(item["snippet"]["title"])
