from __future__ import unicode_literals

from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch



def dwnld(song_name : str,tracknum:int):
    results = YoutubeSearch(song_name,max_results=1).to_dict()[0]    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist':'true',
        'quiet':"true",
        
        'outtmpl': f"{tracknum}.mp3",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
            
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download("https://youtube.com"+results["url_suffix"])
    return results["title"]    
        
