import os
import asyncio
import discord
from discord.ext import commands
import youtube


client = commands.Bot(command_prefix='.')
current_tracks = {}
current_playing_track_no = 0
track_num = 0




for i in os.listdir():
    if i.endswith('.mp3'):
        try:
            os.remove(i)
        except Exception:
            pass 


@client.event
async def on_ready():
    print('All OK!')        

def music_downloader(song_name:str):
    return youtube.dwnld(song_name,track_num)

def next_song(ctx: commands.context.Context):
    global current_playing_track_no
    if current_playing_track_no < track_num:
        current_playing_track_no +=1
        asyncio.run_coroutine_threadsafe(player(ctx, current_tracks[track_num],current_playing_track_no), client.loop)





async def player(ctx : commands.context.Context,song_name:str,track_to_play:int):
    global current_playing_track_no
    await ctx.send(f"Playing...{song_name}",delete_after=5)  
    try:        
        vc.play(discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source=f"C:\\Users\\rohan\\OneDrive\\PYTHON\\Discord_Bot\\{track_to_play}.mp3"),after = lambda fnc: next_song(ctx))
        print(current_playing_track_no)
    except Exception:
        current_playing_track_no -= 1
        print("\nError while playing the song!\n")
    
         
    


@client.command()
async def play(ctx : commands.context.Context, *song_name: str):
    global track_num,vc, current_playing_track_no
    if ctx.author.voice is not None:
        if ctx.voice_client is None: 
            vc = await ctx.author.voice.channel.connect()
            track_num +=1
            current_playing_track_no +=1
            await ctx.send(f'Wait...',delete_after=5)
            song_name = " ".join(song_name)
            try:
                current_tracks[track_num] = music_downloader(song_name)
                await player(ctx,song_name,track_num)
            except Exception:
                await ctx.send('Song Not Found!')
                track_num -=1
                     
               
            
            
        else:
            if ctx.voice_client.is_playing():
                track_num +=1
                await ctx.send("Added to Playlist!",delete_after=5)
                try:
                    current_tracks[track_num] = music_downloader(" ".join(song_name))
                except Exception:
                    track_num -=1
                    ctx.send("Try again!",delete_after=5)
            else:
                track_num +=1
                await ctx.send(f'Wait...',delete_after=5)
                song_name = " ".join(song_name)
                try:
                    current_tracks[track_num] = music_downloader(song_name)
                    await player(ctx,song_name,track_num)
                except Exception:
                    await ctx.send('Song Not Found!')
                    track_num -=1

    else:
        await ctx.send("Join a voice channel!",delete_after=5)





@client.command()
async def pause(ctx):
    try:
        await ctx.voice_client.pause()
    except Exception:
        pass    
@client.command()
async def resume(ctx):
    try:
        await ctx.voice_client.resume()
    except Exception:
        pass
@client.command()
async def stop(ctx):
    try:
        await ctx.voice_client.disconnect()
        for i in os.listdir():
            if i.endswith('.mp3'):
                os.remove(i)
    except Exception:
        pass

@client.command()
async def playlist(ctx):
    playlist_str = ""
    for i in current_tracks.keys():
        playlist_str += f"{i}. {current_tracks[i]}\n"
    await ctx.send(playlist_str)


@client.command()
async def next(ctx):
    try:
        if current_playing_track_no < track_num:
            ctx.voice_client.stop()
            next_song(ctx)

    except Exception:
        pass    


@client.command()
async def prev(ctx):
    global current_playing_track_no,track_num
    try:
        if (current_playing_track_no <= track_num) and current_playing_track_no != 1:
            ctx.voice_client.stop()
            current_playing_track_no -=1
            await player(ctx, current_tracks[current_playing_track_no],current_playing_track_no)
            

    except Exception:
        pass        


client.run(os.getenv("disc_token"))
