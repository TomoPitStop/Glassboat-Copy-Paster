import os, easygui, shutil, time
'''
This script looks at one directory, takes files with a specific beginning (RTM_ RDE_ and BND_ files), 
creates new folders in a second directory with that same beginning (RTM_215_01, RDE_019_01 etc) and then copies and pastes them over 
e.g all files starting in RTM_215_01 will be copied over to a new directory, pasted within a folder named by that scene RTM_215_01
They'll be copied in the same folder structures - charactername / MASTERED/RAW/VIDEO// 
And _v2s etc. put into alts folders 
'''
# This checks if the file is an alt. Checks for _v in the last 8 characters only, so it will catch _V20.mov but ignore a file called battle_victory.wav
def altCheck(_file,_subFolder):
    _fileEnd = _file[-8:] 
    if '_v' in _fileEnd:
        return _subFolder + '\\Alts'
    else:
        return _subFolder

current_working_directory = easygui.diropenbox("Choose where you're copying files from (e.g the character's delivery or rendered folder)", 'Choose location')
final_directory = easygui.diropenbox("Choose where you're copying files to (e.g the Cutscene Sessions folder)", 'Choose destination')
newVideoExtension = easygui.buttonbox('Choose the desired video extension', 'Choose video extension', choices = ['.mov', '.mp4'])

print('Started at ' + time.asctime())

if newVideoExtension == '.mov':
    oldVideoExtension = '.mp4'
elif newVideoExtension == '.mp4':
    oldVideoExtension = '.mov'


for root, dirs, files in os.walk(current_working_directory):
    for file in files:
        # Below Renames old video extension to new
        if (file.endswith(oldVideoExtension)):
            newFilename = str(file[:-4]) + newVideoExtension
            os.rename(root + '\\' + file, (root + '\\' + newFilename))
            file = newFilename

        if (file.endswith(newVideoExtension) or file.endswith(".wav")):
            folders = root.split('\\')

            # Finds where the rtm_ folder is and defines this is a variable (rtm_folder_count). This will be used later, stepping up or down the folders list
            # to find the charactername and subfolder (mastered, raw etc). Doing it like this means you can reuse this script and search for a different string 
            # e.g swap out Gunboat's 'rtm_separate' for 'Cutscene' in another project
            for folderIndex, folderName in enumerate(folders):
                if 'rtm' in folderName:
                    rtm_folder_count = folderIndex

            # Searches for rtm_separate folder and searches for files with R or B (Gumbo cutscene files always start RTM_ RDE_ or BND_)
            for folder in folders:
                    if folder.startswith('rtm_'):
                        if file.startswith('R') or file.startswith('B'):
                   
                            # This takes the first 10 characters of a file 'RTM_215_01' and calls this cutsceneName - will be used for our new folders.
                            cutsceneName = file[:10]

                            # Counts from the rtm_folder locations to find the character name and the subfolder (mastered or raw etc)
                            characterName = folders[rtm_folder_count - 2]
                            subFolder = folders[rtm_folder_count - 1]   
                            # Checks if file is an alt
                            subFolder = altCheck(file,subFolder)
                                        
                            # Catching any video files in MASTERED, when these should actually be in VIDEOS, and moving them to VIDEOS
                            # This will only catch files in a folder called exactly MASTERED so this could be improved / could need double checking.
                            if folders[rtm_folder_count - 1] == 'MASTERED' and file.endswith(newVideoExtension):
                                subFolder = 'VIDEOS'
                                # Checks if file is an alt
                                subFolder = altCheck(file,subFolder)

                            os.makedirs((final_directory + '\\' + cutsceneName + '\\' + characterName + '\\' + subFolder), exist_ok=True)

                            shutil.copy(root + '\\' + file, final_directory + '\\' + cutsceneName + '\\' + characterName + '\\' + subFolder + '\\' + file) 

print('Completed at ' + time.asctime())

    ### Improvements ###
    ### DONE ###
    # Change any .mov to .mp4 and vice versa - with a button box to choose which you want
    # Improve the _v search function for alts (search last 4 digits only) - to defend against a file being called battle_victory or something
    # If finds a video in MASTERED, move it to VIDEOS 
    # It's a pain having to count where the characterName folder is. Could this be better?