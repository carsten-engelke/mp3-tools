# Merge mp3 files from the current directory or from subfolders (each into one mp3 file)
# Carsten Engelke 2018 under MIT-license.
# version:
#    0.1.0  initial port from windows script, introducing automation
#    0.2.0  bug corrected foobar needs to be called from working directory as the command line plugin cannot handle empty
#           spaces in file names or paths given by command line
#    1.0.0  first automated working version, migrated to vs code

import os
import subprocess
import sys
import time
from os.path import basename

import natsort
from _thread import start_new_thread
from pynput.keyboard import Controller, Key

print ("merge-mp3 0.2.0 (C)opyright Carsten Engelke 2018")
print ("Use: python merge-mp3.py [dir] [sub] [foobarpath] [mp3tagpath] [autowaittime]")
print ("    [dir] determines the directory in which to perform the script. Use '.' to select the current directory")
print ("    [sub] determines wheter all mp3 files in subfolders should be merged into one file each. ('true' to do so)")
print ("    [foobarpath] determines the path to your foobar2000 installation. Please provide in case it differs from 'C:/Program Files (x86)/foobar2000/foobar2000.exe'")
print ("    [mp3tagpath] determines the path to your mp3tag installation. Please provide in case it differs from 'C:/Program Files (x86)/Mp3tag/Mp3tag.exe'")
print ("    [autowaittime] determines whether to automatically clos foobar2000 after some seconds. Use -1 to disable and any number to set the waiting time.")

def mergesubdirs(dir, foobarpath, autowaittime):
    filelist = []
    with os.scandir(dir) as it:
        for subdir in it:
            if (not subdir.name.startswith(".") and subdir.is_dir()):
                aimfile = mergedir(subdir, True)
                if (aimfile != None):
                    filelist.append(aimfile)
    callfoobar(foobarpath, dir, filelist, autowaittime)
    print ("Merging subdirectories of " + dir + " done.")

def mergedir(dir, copytoparent):
    if (copytoparent):
        filestr = os.path.dirname(dir.path) + os.sep + dir.name + ".mp3"
    else:
        filestr = os.path.dirname(dir) + os.sep + os.path.basename(dir) + ".mp3"
    mp3number = " ".join(os.listdir(dir)).count(".mp3")
    mp3now = 0
    if (mp3number > 0):
        print ("mp3 file found. Merging to: " + filestr + "...0%\r", end=" ", flush=True)
        if (os.path.exists(filestr)):
            os.remove(filestr)
        with open(filestr, "ab") as aimfile:
            with os.scandir(dir) as it:
                for f in it:
                    if (f.name.endswith(".mp3") and f.is_file()):
                        mp3now += 1
                        srcfile = open(f, "rb")
                        aimfile.write(srcfile.read())
                        # print ("mp3 file found. Merging to: " + filestr + "..." + str(mp3now*100 // mp3number) + "%\r", end=" ", flush=True)
            # print ("mp3 file found. Merging to: " + filestr + "...done")
            return aimfile
    else:
        print ("No mp3 in '" + dir.path + "' found.")
        return None

def callfoobar(foobarpath, workdir, filelist, autowaittime):
    # if ("".join(filelist).count(" ") > 0):
    #     print ( "foobar2000 can't handle files or directories containing empty space characters. Please check stream repair manually.")
    #     return False
    # else:
    #     print ("nothing found...")
    filenamelist = []
    for f in filelist:
        filenamelist.append(f.name)
    rebuildcmdlist = [foobarpath]
    rebuildcmdlist.append("/runcmd-files=Util/Rebuild")
    rebuildcmdlist.extend(filenamelist)
    fixcmdlist = [foobarpath]
    fixcmdlist.append("/runcmd-files=Util/Fix")
    fixcmdlist.extend(filenamelist)
    minimizecmdlist = [foobarpath]
    minimizecmdlist.append("/runcmd-files=Utilities/Optimize file layout + minimize file size")
    minimizecmdlist.extend(filenamelist)
    #print ("CHECKPOINT: Rebuild-CMD:" + str(rebuildcmdlist) + "\n    Fix-CMD:" + str(fixcmdlist) + "\n    Min-CMD:" + str(minimizecmdlist))
    os.chdir(workdir)
    if (autowaittime >= 0):
        print ("Calling foobar2000 for rebuilding the mp3 stream. Automatically ending in:" + str(autowaittime*len(filenamelist)), end="...", flush=True)
        start_new_thread(closefoobar, (foobarpath, autowaittime, len(filelist), True))
    else:
        print ("Calling foobar2000 for rebuilding the mp3 stream. Please close the foobar window to continue", end="...", flush=True)
    subprocess.call(rebuildcmdlist)
    print ("done")
    if (autowaittime >= 0):
        print ("Calling foobar2000 for fixing the mp3 metadata length. Automatically ending in:" + str(autowaittime*len(filenamelist)/2), end="...", flush=True)
        start_new_thread(closefoobar, (foobarpath, autowaittime/2, len(filelist), True))
    else:
        print ("Calling foobar2000 for fixing the mp3 metadata length. Please close the foobar window to continue", end="...", flush=True)
    subprocess.call(fixcmdlist)
    print ("done")
    if (autowaittime >= 0):
        print ("Calling foobar2000 for minimizing file. Automatically ending in " + str(autowaittime*len(filenamelist)/3), end="...", flush=True)
        start_new_thread(closefoobar, (foobarpath, autowaittime/3, len(filelist), False))
    else:
        print ("Calling foobar2000 for minimizing file. Please close the foobar window to continue", end="...", flush=True)
    subprocess.call(minimizecmdlist)
    print ("done")
    return True;

def closefoobar(foobarpath, sleeptime, filenumber, press):
    closecmdlist = [foobarpath, "/exit"]
    k = Controller()
    if (press):
        time.sleep(sleeptime)
        k.press(Key.enter)
        k.release(Key.enter)
    time.sleep(sleeptime * filenumber)
    subprocess.call(closecmdlist)

#PROGRAM ENTRY POINT
foobarpath = "C:/Program Files (x86)/foobar2000/foobar2000.exe"
mp3tagpath = "C:/Program Files (x86)/Mp3tag/Mp3tag.exe"
decisionset = False
mergesub = True
dir = os.getcwd()
autowaittime = 3

if (len(sys.argv) > 1 and sys.argv[1] != "."):
    if (os.path.isdir(sys.argv[1])):
        dir = sys.argv[1]
    else:
        i = ""
        while (i != "y" and i != "n" and i != "Y" and i != "N"):
            i = input ("Specified directory not found: " + sys.argv[1] + " ... will use current directory instead: " + dir + "...OK? (Y)es or (N)o?")
            if (i == "n" or i == "N"):
                sys.exit(0)

if (len(sys.argv) > 2):
    decisionset = True
    if (sys.argv[2] == "true" or sys.argv[2] == "True"):
        mergesub = True;
    else:
        mergesub = False

if (len(sys.argv) > 3 and sys.argv[3] != "."):
    foobarpath = sys.argv[3]
    
if (len(sys.argv) > 4 and sys.argv[4] != "."):
    mp3tagpath = sys.argv[4]

if (len(sys.argv) > 5):
    autowaittime = int(sys.argv[5])

while (not decisionset):
    i = input("Merge (S)ubfolders or this (D)irectory or (A)bort?")
    if (i == "S" or i == "s"):
        mergesub = True
        decisionset = True
    if (i == "D" or i == "d"):
        mergesub = False
        decisionset = True
    if (i == "A" or i=="a"):
        sys.exit(0)

print ("CHECKPOINT: \n    mergesub: " + str(mergesub) + "\n    dir: " + dir + "\n    foobarpath: " + foobarpath + "\n    autowaittime:" + str(autowaittime))

if (mergesub):
    mergesubdirs(dir, foobarpath, autowaittime)
else:
    aimfile = mergedir(dir, False)
    if (aimfile != None):
        callfoobar(foobarpath, dir, [aimfile], autowaittime)
    print ("Merging mp3s in " + dir + " done.")
