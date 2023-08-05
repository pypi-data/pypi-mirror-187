from tkinter import *
import tkinter.simpledialog
import configparser
import os

class SettingsDialog(tkinter.simpledialog.Dialog):

    def body(self, master):
        self.inifile=getConfig()
        settings=self.inifile["settings"]
        f=("Helvetica",12)
        Label(master, text="Server:",font=f).grid(row=0)
        Label(master, text="Connect:",font=f).grid(row=1)
        self.e1var = StringVar(value=settings.get("Server","example.server.net:8922"))
        self.e2var = StringVar(value=settings.get("Connect","login command here"))
        self.e1 = Entry(master,width=60,font=f,textvariable=self.e1var)
        self.e2 = Entry(master,width=60,font=f,textvariable=self.e2var)
        self.fontvar=StringVar()
        Label(master,text="Font Size:",font=f).grid(row=2)
        self.spinbox=Spinbox(master,font=f,values=("6","8","10","12","14","16","18","20"),textvariable=self.fontvar)
        self.fontvar.set(settings.get("fontsize","12"))
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.spinbox.grid(row=2,column=1,sticky=W)

        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        print(first, second)
        self.result=(first,second)
        settings=self.inifile["settings"]
        settings["Server"]=first
        settings["Connect"]=second
        settings["Fontsize"]=self.fontvar.get()
        saveConfig(self.inifile)

def getConfigFile():
    return os.path.expanduser("~/moocoderpy.ini")

def getConfig():
    inifile=configparser.RawConfigParser()
    inifile.read(getConfigFile())
    if not inifile.has_section("settings"):
        inifile.add_section("settings")
    if inifile.has_section("DEFAULT"):
        inifile.remove_section("DEFAULT")
    if not inifile.has_section("test"):
        inifile.add_section("test")
    if not inifile.has_section("connections"):
        inifile.add_section("connections")
    return inifile

def saveConfig(inifile):
    with open(getConfigFile(),"w") as fp:
        inifile.write(fp)

if __name__ == "__main__":
    
    root=Tk()
    d=SettingsDialog(None,title="MoocoderPy Settings")
    print(d.result)