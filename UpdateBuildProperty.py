import os
import sys
from tkinter import messagebox
import user_new
from user_new import *
from user_new import UpdateProgressBarValue

def ubp(ProjPath, NewVersion, Progress, CreatedNewXml=0, UpdateHudson=0):
    #Finding build.properties file
    ProjName = ProjPath.split("\\")[-1]
    UpdateProgressBarValue(Progress, ProjName , "blue")
    UpdateProgressBarValue(Progress, "#-----Input data Received-----#" , "blue")
    print_log_str = "Project path: "+ProjPath+"\nNew Version: "+NewVersion
    UpdateProgressBarValue(Progress, print_log_str, "blue")
    UpdateProgressBarValue(Progress, "#-----Input data End-----#\n" , "blue")
    UpdateProgressBarValue(Progress, "Input validation successful" , "green")
    ProjPath = ProjPath + "\\build\\build-config"
    try:
        list_of_files = os.listdir(ProjPath)
    except Exception as e:
        print(e)
        messagebox.showerror("ERROR","Invalid directory : "+ ProjPath)
        user_new.UpdateProgressBarValue(Progress, "Invalid directory :\n"+ ProjPath, "red")
        return 0
    checkBuildFilePresence = False
    for your_file_name in list_of_files:
        if( your_file_name == 'build.properties'):
            checkBuildFilePresence=True
    
    if not checkBuildFilePresence:
        print("build.propertied could not found at : ", ProjPath)
        messagebox.showerror("ERROR","build.propertied could not found at : "+ ProjPath)
        user_new.UpdateProgressBarValue(Progress, "build.propertied could not found at :\n"+ ProjPath, "red")
        return 0
    BuildFileContents = []
    BuildFileLoc= ProjPath + "\\build.properties"
    print("build.properties file found at ", BuildFileLoc)
    f = open(BuildFileLoc, "r")
    #getting all file lines in the FileLines list
    FileLines= f.readlines()
    #Iterating on FileLines to find "component.version=1.0.46" line
    for index, SingleLine in enumerate(FileLines):        
        ValueField = SingleLine.split("=")  #Used split to find "component.version" field
        if(ValueField[0] == "component.version"):
            oldVersion = ValueField[1]
            print("Old version is", ValueField[1])
            ValueField[1] = NewVersion +"\n"
            FileLines[index]= ValueField[0] + "=" + str(ValueField[1])
            print("--------- Version updated ---------" , ValueField[1])
            user_new.UpdateProgressBarValue(Progress, "build.properties : Version changed from "+oldVersion+" to "+NewVersion, "green")
        elif(ValueField[0] == "hudson.server"):
            print("Changing Hudson server value. Old hudson value was : ", ValueField[1])
            ValueField[1] = "http://frdrpsrv8071.france.intra.corp:8081/hudson/" +"\n"
            FileLines[index]= ValueField[0] + "=" + str(ValueField[1])
            user_new.UpdateProgressBarValue(Progress, "Hudson value updating to http://frdrpsrv8071.france.intra.corp:8081/hudson/", "green")
        BuildFileContents.append(SingleLine)
    f.close()
    # Opening file to clear all file data
    f=open(BuildFileLoc, "w")
    f.write("")
    f.close()
    # Appending data into a blank file
    write_file=open(BuildFileLoc, "a")
    for item in FileLines:
        write_file.write(item)
    print("File written successfully")
    UpdateProgressBarValue(Progress, "build.properties file updated successfully." , "green")
    write_file.close()
    return 1