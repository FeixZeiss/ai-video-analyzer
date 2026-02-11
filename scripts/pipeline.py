import argparse
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from ai_video_analyzer.config import (
    get_token_path,
    get_client_secret_path,
    require_file,
    ensure_parent_dir
)

from ai_video_analyzer.llm.SummaryGenerator import CommentGenerator
from ai_video_analyzer.yt.ChannelStorage import ChannelStorage
from ai_video_analyzer.yt.Videogetter import Videogetter


SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze YouTube videos and create German summaries."
    )
    parser.add_argument(
        "--channel",
        action="append",
        dest="channels",
        help="YouTube channel name. Can be used multiple times. Default: Fireship.",
    )
    parser.add_argument(
        "--since-date",
        type=str,
        default=None,
        help="Only analyze videos published on/after this date (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--max-videos",
        type=int,
        default=None,
        help="Analyze at most N videos (newest first).",
    )
    parser.add_argument(
        "--new-only",
        action="store_true",
        help="Only analyze videos not yet present in the cache.",
    )
    parser.add_argument(
        "--summary-format",
        choices=["paragraph", "sections"],
        default="paragraph",
        help="Output format for generated summaries.",
    )
    return parser.parse_args()


def parse_published_at(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_since_date(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("--since-date must be in format YYYY-MM-DD") from exc
    return parsed.replace(tzinfo=timezone.utc)


def filter_videos(
    videos: List[Dict[str, Any]],
    since_date: Optional[datetime],
    max_videos: Optional[int],
) -> List[Dict[str, Any]]:
    filtered = videos

    if since_date is not None:
        filtered = [
            v for v in filtered
            if (parse_published_at(v.get("published_at", "")) or datetime.min.replace(tzinfo=timezone.utc)) >= since_date
        ]

    filtered = sorted(
        filtered,
        key=lambda v: parse_published_at(v.get("published_at", "")) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    if max_videos is not None:
        filtered = filtered[:max_videos]

    return filtered


def format_summary_text(summary: str) -> str:
    """
    Improves readability by placing each sentence on a new line.
    Existing line breaks are preserved.
    """
    lines: List[str] = []
    for raw_line in summary.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        sentences = re.split(r"(?<=[.!?])\s+", line)
        lines.extend([s.strip() for s in sentences if s.strip()])
    return "\n".join(lines)


def get_credentials() -> Credentials:
    token_path = get_token_path()
    client_secret_path = require_file(get_client_secret_path(), "client_secret.json")

    if token_path.exists():
        return Credentials.from_authorized_user_file(str(token_path), SCOPES)

    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
    credentials = flow.run_local_server(port=0)

    ensure_parent_dir(token_path)
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(credentials.to_json())

    return credentials


def main() -> None:
    args = parse_args()

    if args.max_videos is not None and args.max_videos <= 0:
        raise ValueError("--max-videos must be > 0")
    since_date = parse_since_date(args.since_date) if args.since_date else None

    credentials = get_credentials()
    youtube = build("youtube", "v3", credentials=credentials)

    loader = ChannelStorage(youtube)
    channels = args.channels or ["Fireship"]
    for channel_name in channels:
        loader.add_Channel_By_Name(channel_name)

    videogetter = Videogetter(loader.get_Channels(), youtube)
    videogetter.get_Upload_IDs()

    if args.new_only:
        videoInformation = videogetter.getNewInformation()
    else:
        videoInformation = videogetter.getInformation()
        videogetter._save_cache(videoInformation)

    videoInformation = filter_videos(
        videoInformation,
        since_date=since_date,
        max_videos=args.max_videos,
    )

    print(f"Videos selected for analysis: {len(videoInformation)}")
    gen = CommentGenerator()
    commentDict: Dict[str, Dict[str, Any]] = {}

    for info in videoInformation:
        video_title = info["title"]
        statement = info["description"]
        tags = info.get("tags", [])

        comment = gen.generate_summary(
            video_title,
            statement,
            tags=tags,
            output_format=args.summary_format,
        )
        commentDict[info["video_id"]] = {
            "title": video_title,
            "published_at": info.get("published_at", ""),
            "summary": format_summary_text(comment),
        }
        print("created comment for video:", info["video_id"])

    with open("Summaries.json", "w", encoding="utf-8") as f:
        json.dump(commentDict, f, ensure_ascii=False, indent=2)



if __name__ == "__main__":
    main()
