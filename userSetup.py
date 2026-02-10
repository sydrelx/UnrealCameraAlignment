#    
#Setup for Unreal Camera Tool to work within Autodesk MAYA's GUI
#    

import os, shutil, subprocess, sys
import maya.cmds as cmds
import maya.mel as mel
import maya.utils as utils



## ONLY THING YOU NEED TO CHANGE TO GET TOOL TO WORK IS THE LOCATION OF THE SCRIPTS

scriptsFolder = "C:/Users/user/Documents/maya/scripts" ## wherever the scripts folder is going to be, change the file path here

# Nothing else needs to be changed within this script for it to run properly

print("Using scriptsFolder"+scriptsFolder)

if scriptsFolder in sys.path:
    print( '' )
else:
    sys.path.append(scriptsFolder)
        
###  Creates Menu UI  ###
def us_createScriptsMenu(scriptsFolder):
    
    if cmds.menu('scriptsMenu', exists=1):
        cmds.deleteUI('scriptsMenu')
    
    if scriptsFolder in sys.path:
        print( '' )
    else:
        sys.path.append(scriptsFolder)
    
    scriptsMenu = cmds.menu('scriptsMenu', p='MayaWindow', to=1, aob=1, l='Scripts')
    cmds.menuItem(p=scriptsMenu, l="Update Menu")
    cmds.menuItem(p=scriptsMenu, l="Change Directory")
    cmds.menuItem(p=scriptsMenu, d=1)
        
    absoluteFiles = []
    relativeFiles = []
    folders = []
    allFiles = []
    currentFile = ''
    excludedFiles = ['userSetup.py']
    
    for root, dirs, files in os.walk(scriptsFolder):
        for x in files:
            if x in excludedFiles:
                continue
            correct = root.replace('\\', '/')
            currentFile = (correct + '/' + x)
            allFiles.append(currentFile)
            if currentFile.endswith('.mel'):
                relativeFiles.append(currentFile.replace((scriptsFolder + '/'), ""))
            if currentFile.endswith('.py'):
                relativeFiles.append(currentFile.replace((scriptsFolder + '/'), ""))

        for d in dirs:
            print( d )
            otherPath = scriptsFolder +'/'+ d
            sys.path.append(otherPath)
                        
    relativeFiles.sort()
    
    for relativeFile in relativeFiles:
        split = relativeFile.split('/')
        fileName = split[-1].split('.')
        print(split)
        i=0
        while i<(len(split)):
            ### Create Folders ###
            if i==0 and len(split) != 1:
                if cmds.menu(split[i] ,ex=1) == 0:
                    cmds.menuItem(split[i], p=scriptsMenu, bld=1, sm=1, to=1, l=split[i])
            if i > 0 and i < (len(split)-1):
                if cmds.menu(split[i] ,ex=1) == 0:
                    cmds.menuItem(split[i], p=split[i-1], bld=1, sm=1, to=1, l=split[i])
            
            ### Create .mel Files  ###
            if fileName[-1] == 'mel':
                if i==len(split)-1 and len(split) > 1:
                    scriptName = split[-1].split('.')
                    temp1 = 'source ' + '"' + scriptsFolder + '/' + relativeFile + '"; ' + scriptName[0]
                    command = '''mel.eval(''' + "'" + temp1 + '''')'''
                    cmds.menuItem(split[i], p=split[i-1], c=command, l=split[i])
                if i==len(split)-1 and len(split) == 1:
                    scriptName = split[-1].split('.')
                    temp1 = 'source ' + '"' + scriptsFolder + '/' + relativeFile + '"; ' + scriptName[0]
                    command = '''mel.eval(''' + "'" + temp1 + '''')'''
                    cmds.menuItem(split[i], p=scriptsMenu, c=command, l=split[i])
                
            ### Create .py Files  ###
            if fileName[-1] == 'py':
                if i==len(split)-1 and len(split) > 1:
                    command = 'import ' + fileName[0] + '\n' + fileName[0] + '.' + fileName[0]+ '()'
                    print( command )
                    #command = 'import ' + fileName[0]  
                    cmds.menuItem(split[i], p=split[i-1], c=command, l=split[i])
                if i==len(split)-1 and len(split) == 1:
                    command = 'import ' + fileName[0] + '\n' + fileName[0] + '.' + fileName[0]+ '()'
                    cmds.menuItem(split[i], p=scriptsMenu, c=command, l=split[i])
            i+=1
            


utils.executeDeferred('us_createScriptsMenu(scriptsFolder)')
