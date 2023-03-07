import os
import subprocess
import shutil

#0 = new
#1 = downloaded
#2 = copy done
#
#
#
#
#7 = error while copying
#8 = error while downloading
#9 = fatal error
# Function to get all files in a folder and its subfolders

def main():
    folder_path = "/home/user/Schreibtisch/SCRPPER/seleniumTest/src/musik/MP3"
    all_files = get_all_files(folder_path,include="-_0.mp3")
    for file_path in all_files: 
        try:
            getFlacs()
        except:
            renameStatus(file_path,"9")

def copyFlac(path,dest):
    folder ="/FLAC/" + os.path.dirname(path[5:])
    if not os.path.exists(folder):
        os.makedirs(folder)
        copyOtherFiles(path,folder)
    source = get_all_files("/download")
    dest = folder + os.path.basename(path)
    shutil.copy2(source,dest)
    
def copyOtherFiles(src,dest):
    files = get_all_files(src,execlude=".mp3")
    for file in files:
        shutil.copy2(file,dest)
        filename = os.path.basename(file)
        if filename.endswith(".m3u8"):
            changePlaylist(dest + filename)
def changePlaylist(src,type=".flac"): 
    with open(src, 'r') as f:
       content = f.read()
    # Replace .mp3 with .flac
    if type == ".flac":
        content = content.replace('.mp3', '.flac')
    else: 
        content = content.replace('.flac', '.mp3')
    # Write the updated content back to the file
    with open(src, 'w') as f:
        f.write(content)

def get_all_files(folder_path, include="", execlude=""):
    allFiles = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            allFiles.append(os.path.join(dirpath, filename))
    if len(include) > 1:
        filtertFiles = [txt for txt in allFiles if include in txt]
    if len(execlude) > 1:
        filtertFiles = [txt for txt in allFiles if execlude not in txt]
    allFiles = filtertFiles
    return allFiles


def renameStatus(file_path,status):
        pathSplt = os.path.splitext(file_path)
        filename, extension = pathSplt[0][-1:],pathSplt[1]
        new_file_path = os.path.join(os.path.dirname(file_path), filename+ status + extension)
        os.rename(file_path, new_file_path)

from SeleniumScraper import SeleniumScraper
def getFlacs(file_path):
    fetcher = SeleniumScraper("db")
    remove_folder_contents("/downloads/")
    folder_path = 'mp3s'
    status = "1" if fetcher.downloadFlac(os.path.basename(file_path)) else "8"
    renameStatus(file_path,status)
    if status == "9" : return  
    status = "2" if copyFlac(file_path) else "7"
    renameStatus(file_path,status)

#def checkValidSoundFile():

def remove_folder_contents(folder_path):
    """Removes all files and directories in the given folder using 'rm -rf *' shell command"""
    subprocess.run(["rm", "-rf", folder_path + "/*"])