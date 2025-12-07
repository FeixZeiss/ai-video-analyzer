from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

class ChannelStorage():
    """
    class to work with Videochannels
    """
    def __init__(self, youtube):
        self.channels = {}
        self.youtube = youtube
        
    """
    returns channelID 
    throws Exception if Channel wasn't found
    """
    def get_ChannelID(self,channelName):
        print("trying to add Channel")
        request = self.youtube.search().list(
            q=channelName,
            type="channel",
            part="id,snippet",
            maxResults=1
        )
        response = request.execute()
        if not response["items"]:
            raise Exception(f"No Youtube Channel found for '{channelName}'")
        return response["items"][0]["id"]["channelId"]
    
    """
    adds a ChannelID to the List
    """
    def add_Channel_By_Name(self, name):
        if name in self.channels:
            print(f"Kanal '{name}' already exists.")
            return
        channel_ID = self.get_ChannelID(name)
        self.channels[name] = channel_ID

    """
    returns List of all Channels
    """
    def get_Channels(self):
        return self.channels
        