import tkinter
from tkinter import * # type: ignore
from tkinter import messagebox
import UpdateBuildProperty, UpdateReleaseFolder
from UpdateBuildProperty import * # type: ignore
from UpdateReleaseFolder import * # type: ignore
from tkinter import ttk
import  customtkinter
import datetime



def ValidateVersionValue(input):
    #ValidateVersionValue Checking of version input contains only numbers or not
    list = input.split(".")
    flag= True
    for i in list:
        if i.isnumeric():
            pass
        else:
            flag= False
            break
    return flag


list_progress = []

def UpdateProgressBarValue(frame1, value, colour):
    #Printing progress in 2nd window. getting call from UdateBuildProperty.py & UpdateReleaseFolder.py
    label2 = customtkinter.CTkLabel(frame1, text=value, text_color=colour, font=("Arial", 13))
    list_progress.append(label2.cget("text"))
    # print("Printing progress list ",list_progress)
    label2.pack()

def AdddButtons(frame1, ProgressWindow):
    print("-------------------------------------")
    button1 = customtkinter.CTkButton(master=ProgressWindow, text="close", command= ProgressWindow.destroy)
    button1.pack(pady=12, padx=10)
    button2 = customtkinter.CTkButton(master=ProgressWindow, text="Export to file", command= ExportToFile)
    button2.pack(pady=12, padx=10)
    
def ExportToFile():
    # Create folder "VersionUpgraderLogs" in Program Files if doesn't exists
    newpath = r'C:\\VersionUpgraderLogs\\' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    #Creating filename as projectName_timestamp
    filename = list_progress[0]+"_"+ datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
    Fullfilepath = str(newpath)+str(filename)
    print("Full file path is : ", Fullfilepath)
    with open(Fullfilepath, "w") as f:
        for val in list_progress:
            f.write(val)
            print("Progress data: ", val)
            f.write("\n")
        f.write("---Logging completed---")  
    print("Completed file writing")


def printval():
    global ProjPathval
    global NewVersionval
    # global CreatedNewXmlval
    # global UpdateHudsonval_g
    global ProjName
    ProjPathval_local = ProjPath.get()
    ProjPathval = ProjPathval_local
    ProjName = ProjPathval_local.split("\\")[-1]
    NewVersionval_local = NewVersion.get()
    NewVersionval = NewVersionval_local
    CreatedNewXmlval_local =0  #For checkbox use get()
    # CreatedNewXmlval = CreatedNewXmlval_local
    UpdateHudsonval_local = 0
    # UpdateHudsonval_g = 0


    #checking whether ProjPathval & NewVersionval is empty 
    if(len(ProjPathval_local) == 0):
        messagebox.showerror("ERROR","Please enter Project path value")
    elif(len(NewVersionval_local) == 0):
        messagebox.showerror("ERROR","Please enter New version value")
    elif(not ValidateVersionValue(NewVersionval_local)):
        messagebox.showerror("ERROR","Please enter a numeric value for New version field")        
    else:
        print("Values received:\nProject path : ", ProjPathval_local, "\nNew version :", NewVersionval_local, "\nCreated new XML files :", CreatedNewXmlval_local, "\nUpdate hudson value: ", UpdateHudsonval_local)
        global ProgressWindow
        #Generating 2nd window to print updates
        ProgressWindow = customtkinter.CTkToplevel(window)
        ProgressWindow.geometry("700x400")
        ProgressWindow.title("Progress..")
        customtkinter.set_appearance_mode("green")
        global frame1
        frame1 = customtkinter.CTkScrollableFrame(master=ProgressWindow)
        frame1.pack(pady=20, padx = 60, fill = "both")
        UpdateProgressBarValue(frame1, ProjName , "blue")
        print("ProjName field is :" ,list_progress[0])
        
        #Checking if given project path exist or not
        isExistPath= os.path.exists(ProjPathval_local)
        if ProjPathval_local[-1] == '\\':
            ProjPathval_local=ProjPathval_local[:-1]
        if not isExistPath:
            messagebox.showerror("ERROR","Mentioned Project path does not exists.")
            UpdateProgressBarValue(frame1, "Mentioned Project path does not exists.\n"+ProjPathval_local, "red")
            # exit()
            AdddButtons(ProgressWindow, ProgressWindow)
        else:
            result=UpdateBuildProperty.ubp(ProjPathval_local,NewVersionval_local,frame1, CreatedNewXmlval_local,UpdateHudsonval_local)
            if result:
                UpdateReleaseFolder.urf(ProjPathval_local,NewVersionval_local,frame1, ProgressWindow , CreatedNewXmlval_local)
            if not result:
                AdddButtons(ProgressWindow, ProgressWindow)
                
if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("green")
    window = customtkinter.CTk()
    window.geometry("620x400")
    window.title("Tibco Version Modifier")
    
    frame = customtkinter.CTkFrame(master=window)
    frame.pack(pady=20, padx = 60, fill = "both" ,  expand = True)
    
    label = customtkinter.CTkLabel(master = frame, text="Tibco version modifier", font=("Roboto",24))
    label.pack(pady=12, padx=10)
    
    ProjPath = customtkinter.CTkEntry(master = frame, placeholder_text="Enter Project Path", )
    ProjPath.pack(pady=12, padx=10)
    NewVersion = customtkinter.CTkEntry(master = frame, placeholder_text="Enter New Version", )
    NewVersion.pack(pady=12, padx=10)
    
    # CreatedNewXml = IntVar()
    # UpdateHudson = IntVar()
    # Checkbox = customtkinter.CTkCheckBox(master=frame, text = "Created new XML", variable=CreatedNewXml)
    # Checkbox.pack(pady=12, padx=10)
    # Checkbox = customtkinter.CTkCheckBox(master=frame, text = "Update Hudson value", variable=UpdateHudson)
    # Checkbox.pack(pady=12, padx=15)
    
    button = customtkinter.CTkButton(master=frame, text="Submit", command=printval)
    button.pack(pady=12, padx=10)
    
    close_button = customtkinter.CTkButton(master=frame, text="Close", command=window.destroy)
    close_button.pack(pady=6, padx=10)
   
    window.mainloop()

