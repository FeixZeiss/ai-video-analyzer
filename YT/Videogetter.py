import json
import os

class Videogetter:
    """
    class to get information about YT Videos
    """
    def __init__(self, channels, youtube):
        self.channels = channels 
        self.youtube = youtube
        self.uploads_playlist_id = []
        with open("videos.json", "r", encoding="utf-8") as file:
            self.videoInformation = json.load(file)

    """
    extracts Uploadplaylist IDS of all channels
    """
    def get_Upload_IDs(self):
        for channel_id in self.channels.values():
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()

            # add The uploads playlist ID for all channel videos
            self.uploads_playlist_id.append(response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"])
    
    # Extracts all information of subscribed Channels
    def getInformation(self):
        videos = []
        next_page_token = None
        for id in self.uploads_playlist_id:
            while True:
                # Step 2: get up to 50 videos from the playlist
                playlist_request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()


                # collect all video IDs
                video_ids = [item["contentDetails"]["videoId"] for item in playlist_response["items"]]

                # Step 3: fetch detailed info for these IDs
                video_req = self.youtube.videos().list(
                    part="snippet",
                    id=",".join(video_ids)
                )
                video_resp = video_req.execute()

                for video in video_resp["items"]:
                    snippet = video["snippet"]
                    video_data = {
                        "video_id": video["id"],
                        "title": snippet["title"],
                        "published_at": snippet["publishedAt"],
                        "description": snippet.get("description", ""),
                        "tags": snippet.get("tags", [])
                    }
                    videos.append(video_data)

                next_page_token = playlist_response.get("nextPageToken")
                if not next_page_token:
                    break

        return videos
    
    def getNewInformation(self):
        existing_ids = set()
        filename = "videos.json"
        videos = []

        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                try:
                    saved_videos = json.load(file)
                    existing_ids = {v["video_id"] for v in saved_videos}
                except json.JSONDecodeError:
                    print("Warnung: videos.json ist beschädigt oder leer — starte neu.")
                    saved_videos = []
        else:
            saved_videos = []

        # === 2️⃣ Neue Videos aus allen Upload-Playlists abrufen
        for id in self.uploads_playlist_id:
            next_page_token = None
            while True:
                playlist_request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                # Video-IDs aus Playlist abrufen
                video_ids = [item["contentDetails"]["videoId"] for item in playlist_response["items"]]

                # Nur IDs weiterverarbeiten, die noch nicht in existing_ids sind
                new_ids = [vid for vid in video_ids if vid not in existing_ids]
                if not new_ids:
                    next_page_token = playlist_response.get("nextPageToken")
                    if not next_page_token:
                        break
                    continue

                # Details nur für neue Videos abrufen
                video_req = self.youtube.videos().list(
                    part="snippet",
                    id=",".join(new_ids)
                )
                video_resp = video_req.execute()

                for video in video_resp["items"]:
                    snippet = video["snippet"]
                    video_data = {
                        "video_id": video["id"],
                        "title": snippet["title"],
                        "published_at": snippet["publishedAt"],
                        "description": snippet.get("description", ""),
                        "tags": snippet.get("tags", [])
                    }
                    videos.append(video_data)
                    existing_ids.add(video["id"])  # wichtig: ID gleich merken

                next_page_token = playlist_response.get("nextPageToken")
                if not next_page_token:
                    break

            # === 3️⃣ Neue Videos zur Datei hinzufügen
            if videos:
                all_videos = saved_videos + videos
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(all_videos, file, ensure_ascii=False, indent=2)
                print(f"{len(videos)} neue Videos gespeichert.")
            else:
                print("Keine neuen Videos gefunden.")

            return videos


