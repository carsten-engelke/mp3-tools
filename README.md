# mp3-tools
Merge mp3 files and set correct audio length using foobar2000 with an automated python script. These scripts can merge all files in one directory or create one file for each subdirectory.
![merge mp3 files from subdirectories](/mergemp3subdirs.jpg)
 - merge-mp3.py: merging script, works with foobar2000
 - pack-subdirs.py: pack files into grouped subdirectories (good for large audiobooks)
 - unpack-subdirs.py: unpack files from grouped subdirectories (undo pack-subdirs.py)

## Version
1.0.0 release version. Ported to vscode.

0.2.0 bug corrected foobar needs to be called from working directory as the command line plugin cannot handle empty spaces in file names or paths given by command line

0.1.0 initial release. Port from windows script to python, introducing automation

## Requirements
- Python (script was created using python 3.7.0) (https://www.python.org/)
- foobar2000 (https://www.foobar2000.org/)

## Installation
- copy mergeMp3.py into the directory in which the files to merge are contained.
- run the script and follow the instructions, alternatively use the following command line

Command-line-use:
```
python mergeMp3.py [dir] [sub] [foobarpath] [autowaittime]
    [dir] determines the directory in which to perform. Use '.' to select the current directory
    [sub] determines wheter all mp3 files in subfolders should be merged into one file each. ('true' to do so)")
    [foobarpath] determines the path to your foobar2000 installation. Please provide in case it differs from 'C:/Program Files (x86)/foobar2000/foobar2000.exe'
    [autowaittime] determines whether to automatically clos foobar2000 after some seconds. Use -1 to disable and any number to set the waiting time.
```
```
python pack-subdirs.py [group-size] [dir] [filter] [copy-mode]
    [group-size] determines the number of files to put into each directory
    [dir] determines the directory in which to perform the script. Use '.' to select the current directory
    [filter] Filter the file list according to this
    [copy-mode] If 'True', the files are copied into the created subfolders. If 'False' they are moved (Use with caution).
´´´
```
python unpack-subdirs.py [dir] [subdir-filter] [filter] [copy-mode] [remove-dir]")
    [dir] determines the directory in which to perform the script. Use '.' to select the current directory
    [subdir-filter] Filter the subdir list according to this. Use '*' to select any subdirectory
    [filter] Filter the file list according to this
    [copy-mode] If 'True', the files are copied into the parent folder. If 'False' they are moved (Use with caution).
    [remove-dir] If 'True', the subdirectories are deleted. If 'False' they are left as they are.
´´´
