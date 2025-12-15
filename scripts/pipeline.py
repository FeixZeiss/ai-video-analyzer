import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from ai_video_analyzer.config import (
    get_token_path,
    get_client_secret_path,
    require_file,
)

from ai_video_analyzer.llm.CommentGenerator import CommentGenerator
from ai_video_analyzer.yt.ChannelStorage import ChannelStorage
from ai_video_analyzer.yt.Videogetter import Videogetter


SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


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
    credentials = get_credentials()
    youtube = build("youtube", "v3", credentials=credentials)

    loader = ChannelStorage(youtube)
    loader.add_Channel_By_Name("Fireship")

    videogetter = Videogetter(loader.get_Channels(), youtube)
    videogetter.get_Upload_IDs()
    videoInformation = videogetter.getInformation()

    videogetter._save_cache(videoInformation)  

    gen = CommentGenerator()
    commentDict = {}

    for info in videoInformation:
        video_title = info['title']
        statement = info['description']

        comment = gen.generate_summary(video_title, statement)
        commentDict[info['video_id']] = comment 
        
    with open('comments.json', 'w') as f:
        json.dump(commentDict, f)



if __name__ == "__main__":
    main()
