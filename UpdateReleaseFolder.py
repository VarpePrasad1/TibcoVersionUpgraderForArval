import os
import sys
from tkinter import messagebox
import user_new
from user_new import *
import xml.etree.ElementTree as ET
from lxml import etree

AppName = ""
def urf(ProjPath, NewVersion, Progress, ProgressWindow , CreatedNewXml=0):
    global AppName
    AppName = ProjPath.split("\\")[-1]
    print("AppName is ->" , AppName)
    ProjPath = ProjPath + "\\release"
    print("Updated ProjPath : "+ProjPath)
    isExist= os.path.exists(ProjPath)
    if(not isExist):
        print("Release folder does not exist")
        messagebox.showerror("ERROR","Release folder does not exist at : "+ ProjPath)
        user_new.UpdateProgressBarValue(Progress, "Release folder does not exist at :\n "+ ProjPath, "red")
        user_new.AdddButtons(Progress, ProgressWindow)
    else:
        try:
            list_of_files = os.listdir(ProjPath)
            user_new.UpdateProgressBarValue(Progress, "Searching for release folder...", "green")
        except Exception as e:
            print(e)
            messagebox.showerror("ERROR","Failed to open folder : "+ ProjPath)
            sys.exit()
        DirList=os.listdir(ProjPath)   #Fetching files inside Release folder. 
        user_new.UpdateProgressBarValue(Progress, "Opening release folder." , "green")
        print(DirList)
        if len(DirList) == 0:
            messagebox.showerror("ERROR","Release folder is empty.\n Path checked: "+ ProjPath)
            user_new.UpdateProgressBarValue(Progress, "Release folder is empty.\n Path checked: "+ ProjPath, "red")
        user_new.UpdateProgressBarValue(Progress, "Found "+ str(len(DirList))+" elements inside release folder\n" , "green")
        for EveryFolder in DirList:
            FolderPath = ProjPath +'\\' + EveryFolder
            if os.path.isdir(FolderPath):
                #For each folder inside release folder, calling below func
                ans = UpdateBothFiles(FolderPath, Progress, NewVersion)
                if not ans:
                    break
        user_new.AdddButtons(Progress, ProgressWindow)

def UpdateBothFiles(Path, Progress, NewVersion):
    print(Path)
    GetFileList=os.listdir(Path)
    CheckGradle=1
    CheckXML=1
    for iteratoy in GetFileList:
        if iteratoy == 'build.gradle':
            #Build.fradle file found
            CheckGradle =0
        elif iteratoy.endswith(".xml"):
            #Required XML file found
            CheckXML =0
    #Checking below if build.gradle and XML file are present or not
    if CheckGradle and CheckXML:
        messagebox.showerror("ERROR","build.gradle and XML file is not present at "+ Path)
        user_new.UpdateProgressBarValue(Progress, "build.gradle and XML file is not present at:\n"+ Path, "red")
        return 0
    elif CheckGradle:
        messagebox.showerror("ERROR","build.gradle file not present at "+ Path)
        user_new.UpdateProgressBarValue(Progress, "build.gradle file not present at:\n"+ Path, "red")
        return 0
    elif CheckXML:
        messagebox.showerror("ERROR","XML file is not present at "+ Path)
        user_new.UpdateProgressBarValue(Progress, "XML file is not present at:\n"+ Path, "red")
        return 0
    else:
        result=UpdateGradleFile(Path, Progress, NewVersion)
        if result:
            result2=UpdateXMLFile(Path, Progress, NewVersion)
    return result and result2
        
def UpdateGradleFile(Path, Progress, NewVersion):
    FolderName = Path.split("\\")[-1]
    GradleFilePath = Path + "\\build.gradle"
    print("Updating Gradle file: " + FolderName)
    try:
        f= open(GradleFilePath, "r")
    except Exception as e:
        print(e)
        messagebox.showerror("ERROR","Failed to open build.gradle file\n"+ Path)
        return 0
    ReadFile=f.readlines()
    FoundVersion = 1
    for index, EachFields in enumerate(ReadFile):
        if EachFields.startswith("version"):
            ReadFile[index] = 'version "'+ str(NewVersion) +'"\n'
            FoundVersion=0
    if FoundVersion:
        print("Error occured while finding Version inside build.gradle file of - "+FolderName)
        messagebox.showerror("Error occured while finding Version inside build.gradle file of - "+FolderName)
        user_new.UpdateProgressBarValue(Progress, "Error occured while finding Version inside build.gradle file of - "+FolderName , "red")
        return 0
    else:
        f.close()
        try:
            f=open(GradleFilePath, "w")
        except Exception as e:
            print(e)
            messagebox.showerror("ERROR","Failed to update build.gradle file\n"+ Path)
            return 0
        f.write("")
        f.close()
        try:  
            write_file= open(GradleFilePath, "a")
            for item in ReadFile:
                write_file.write(item)
            print(FolderName + " Written successfully")
            user_new.UpdateProgressBarValue(Progress, "build.gradle file updated in : "+FolderName , "green")
        except Exception as e:
            print(e)
            for item in ReadFile:
                write_file.write(item)
            messagebox.showerror("ERROR","Failed to update build.gradle file\n"+ Path)
            return 0
        return 1
    
def UpdateXMLFile(Path, Progress, NewVersion):
    FolderName = Path.split("\\")[-1]
    XmlFilePath = Path + "\\" + FolderName + ".xml"
    print("XML file path :" + XmlFilePath)
    print("Updating XML file: " + FolderName)
    print("Folder name:" , FolderName)
    #Removing last '_BW' from Appname
    UpdatedAppNameWithoutBW = AppName[:-3]
    print("Appname is : " , UpdatedAppNameWithoutBW)
    print("----Updation of XML file starts----")
    try:
        xmlTree = ET.parse(XmlFilePath)
        xmlroot = xmlTree.getroot()
    except Exception as e:
        print(e)
        messagebox.showerror("ERROR","Failed to parse "+FolderName + ".xml file")
        user_new.UpdateProgressBarValue(Progress, "Failed to parse "+FolderName + ".xml file", "red")
        return 0
    print(xmlroot.attrib)
    UpdatedNameAttribute = UpdatedAppNameWithoutBW+'/'+FolderName
    xmlroot.attrib['name'] = UpdatedNameAttribute
    xmlroot.set('name' , UpdatedNameAttribute)
    print("Name attribute updated :" , UpdatedNameAttribute)
    print("New attribute fetching ",xmlroot.attrib)
    print("description element text",xmlroot[1].text)
    for count in range(len(xmlroot)):
        if(xmlroot[count].tag.lower().endswith('description')):
            xmlroot[count].text = "Version "+NewVersion
            print("Found version tag :", xmlroot[count].tag)
        if(xmlroot[count].tag.endswith('NVPairs') and xmlroot[count].attrib['name'] == 'Global Variables'):
            break
    # NVPairs tag found at index number count 
    FindVersionField = "_"+AppName[6:-3]+"/version"
    foundVersion=0
    for FindVersionGV in range(len(xmlroot[count])):
        value=xmlroot[count][FindVersionGV][0].text
        if(value.lower()==FindVersionField.lower()): # type: ignore
            Oldversion = xmlroot[count][FindVersionGV][1].text
            xmlroot[count][FindVersionGV][1].text = NewVersion
            foundVersion=1
            print(FindVersionGV)
            print("Found : ", value, " && OldValue is " , Oldversion , "  && New version is ", NewVersion)
            user_new.UpdateProgressBarValue(Progress, "Changed version from : "+ str(Oldversion)+ " to : " + str(NewVersion) + "  in "+ FolderName, "green")
    if not foundVersion:
        print("Could not found version element in "+FolderName+".xml")
        user_new.UpdateProgressBarValue(Progress, "Could not found version element in "+FolderName+".xml", "red")
    xmlTree.write(XmlFilePath)
    user_new.UpdateProgressBarValue(Progress, FolderName + ".xml file updated of : "+FolderName , "green")
    print("Updation of Release folder done")
    return foundVersion