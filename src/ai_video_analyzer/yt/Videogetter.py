import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class Videogetter:
    """
    Fetches video information from YouTube upload playlists and maintains
    a persistent JSON cache (videos.json) to avoid re-reading already known videos.
    """

    def __init__(self, channels: Dict[str, str], youtube, cache_path: Optional[Path] = None):
        """
        Args:
            channels: dict like {channel_name: channel_id}
            youtube: googleapiclient.discovery.build("youtube", "v3", credentials=...)
            cache_path: optional Path to the cache file (default: data/cache/videos.json in repo root)
        """
        self.channels = channels
        self.youtube = youtube
        self.uploads_playlist_id: List[str] = []

        # Default cache location: <repo_root>/data/cache/videos.json
        self.cache_path: Path = cache_path or (Path.cwd() / "data" / "cache" / "videos.json")

    # ---------- internal helpers ----------

    def _ensure_parent_dir(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    def _load_cache(self) -> List[Dict[str, Any]]:
        if not self.cache_path.exists():
            return []
        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            print("Warning: videos.json cache is corrupted or empty — starting fresh.")
            return []

    def _save_cache(self, all_videos: List[Dict[str, Any]]) -> None:
        self._ensure_parent_dir(self.cache_path)

        # Write atomically-ish: write to tmp then replace
        tmp_path = self.cache_path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(all_videos, f, ensure_ascii=False, indent=2)
        tmp_path.replace(self.cache_path)

    # ---------- public API ----------

    def get_Upload_IDs(self) -> None:
        """
        Extracts the uploads playlist IDs of all channels and stores them in self.uploads_playlist_id.
        """
        self.uploads_playlist_id = []
        for channel_id in self.channels.values():
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()

            self.uploads_playlist_id.append(
                response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            )

    def getInformation(self) -> List[Dict[str, Any]]:
        """
        Fetches *all* videos from all uploads playlists (no caching).
        """
        videos: List[Dict[str, Any]] = []

        for playlist_id in self.uploads_playlist_id:
            next_page_token = None  # IMPORTANT: reset per playlist
            while True:
                playlist_request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                video_ids = [item["contentDetails"]["videoId"] for item in playlist_response.get("items", [])]
                if video_ids:
                    video_req = self.youtube.videos().list(
                        part="snippet",
                        id=",".join(video_ids)
                    )
                    video_resp = video_req.execute()

                    for video in video_resp.get("items", []):
                        snippet = video.get("snippet", {})
                        videos.append({
                            "video_id": video.get("id", ""),
                            "title": snippet.get("title", ""),
                            "published_at": snippet.get("publishedAt", ""),
                            "description": snippet.get("description", ""),
                            "tags": snippet.get("tags", [])
                        })

                next_page_token = playlist_response.get("nextPageToken")
                if not next_page_token:
                    break

        return videos

    def getNewInformation(self) -> List[Dict[str, Any]]:
        """
        Fetches only videos that are not yet present in the cache file.
        Appends new videos to the cache and returns only the newly found videos.
        """
        saved_videos = self._load_cache()
        existing_ids: Set[str] = {v.get("video_id", "") for v in saved_videos if isinstance(v, dict)}

        new_videos: List[Dict[str, Any]] = []

        for playlist_id in self.uploads_playlist_id:
            next_page_token = None
            while True:
                playlist_request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                video_ids = [item["contentDetails"]["videoId"] for item in playlist_response.get("items", [])]
                new_ids = [vid for vid in video_ids if vid and vid not in existing_ids]

                if new_ids:
                    video_req = self.youtube.videos().list(
                        part="snippet",
                        id=",".join(new_ids)
                    )
                    video_resp = video_req.execute()

                    for video in video_resp.get("items", []):
                        snippet = video.get("snippet", {})
                        vid = video.get("id", "")
                        if not vid or vid in existing_ids:
                            continue

                        video_data = {
                            "video_id": vid,
                            "title": snippet.get("title", ""),
                            "published_at": snippet.get("publishedAt", ""),
                            "description": snippet.get("description", ""),
                            "tags": snippet.get("tags", [])
                        }
                        new_videos.append(video_data)
                        existing_ids.add(vid)

                next_page_token = playlist_response.get("nextPageToken")
                if not next_page_token:
                    break

        if new_videos:
            all_videos = saved_videos + new_videos
            self._save_cache(all_videos)
            print(f"{len(new_videos)} new videos saved to cache: {self.cache_path}")
        else:
            print("No new videos found.")

        return new_videos
