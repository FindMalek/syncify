"""
    This module replaces FFMPEG.
    It uses the 'youtubeDownloader' to download and changes the metadata of
    the downloaded track using 'music_tag' and then move it to it's destination
"""

#Importing the module Music-Tag to change the metadata of the audio tracks
import music_tag
from moviepy.editor import *

#Importing the Syncify Youtube Downloader
from downloadHandler.youtubeDownloader import *

#Importing the Syncify System Functions
import os
from SyncifyFunctions.systemFunctions import *

#Import getArtist and isDownloaded function from trackHandeling
from SyncifyFunctions.trackHandeling import getArtists, isDownloaded

#Importing requestHandeling to download the art of the track
from spotifyHandler.requestsHandeling import downloadArt


#Pre-defined path
setting_path = "Settings.json"
download_path = getDataJSON(setting_path, "Settings/Paths/Downloads")
tmpTracks = convertPath("Data/" + os.path.abspath(os.getcwd()))


#Changes all of the metadata of the track
def changeMetaData(path, data):
    #Convert the extension and change the name
    logsSyncify("").Syncify(f"Converting {path} to MP3 file...").debug()
    path = convertAudio(path, data)
    logsSyncify("").Syncify(f"Converted and renamed {path} to MP3 file.").debug()
    
    #Change the meta-data
    logsSyncify("").Syncify(f"Updating the metadata of {path}...").debug()
    audioFile = music_tag.load_file(path)
    print(audioFile)
    """ Fix : KeyError: 'covr' """
    audioFile['tracktitle'] = data['name']
    audioFile['artist'] = getArtists(data)
    audioFile['album'] = data['album']['name']
    audioFile['tracknumber'] = data['track_number']
    audioFile['totaltracks'] = data['album']['total_tracks']
    audioFile['discnumber'] = data['disc_number']
    audioFile['year'] = data['album']['release_date'][:4]
    audioFile['isrc'] = data['external_ids']['isrc']
    logsSyncify("").Syncify(f"Updating the metadata of {path}.").debug()
    
    #Set the artwork
    logsSyncify("").Syncify(f"Setting the artwork of {path}...").debug()
    artPath = downloadArt(data['album']['images'][0]['url'])
    with open(artPath, 'rb') as img:
        audioFile['artwork'] = img.read()
    logsSyncify("").Syncify(f"Set the artwork of {path}.").debug()

    #Change the name of the audio file and save its metadata
    audioFile.save()
    
    #Delete the tmpArt
    os.remove(artPath)
    
    return path
    
#Move the track from /tmp/ to the destination
def moveTrack(currPath, des):
    pass

#Checks if a track is already downloaded or not using the track data
def trackDownloaded(data):
    if(isDownloaded(data['album']['artists'][0]['name'] + ' - ' + data['name'])):
        return True
    else:
        return False

#The main function that changes the metadata of the track and move the track to it's destination
def downloadSyncify(trackData):
    searchTrachData = searchTrack(trackData)
    
    if((trackInYoutube(searchTrachData) == True) and (trackDownloaded(trackData) == False)):
        trackPath = downloadTrack(searchTrachData)
        
        trackPath = changeMetaData(trackPath, trackData)
        #moveTrack(trackPath, destinationPath)
        
    elif((trackInYoutube(searchTrachData) == False) and (trackDownloaded(trackData) == False)):
        #use the spotifyDownloader or raise an error for now
        pass
    
    else:
        #Track is already downloaded
        pass