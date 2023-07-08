import sys
from pythonping import ping
import tkinter as tk
from tkinter import filedialog, Text
from tkinter import *
import os
from configparser import ConfigParser
import subprocess

config = ConfigParser()
config.read(r'test.ini')
currentPrefClient = config.getboolean('DEFAULT', 'openClient')
if currentPrefClient == True:
    os.startfile('C:\Riot Games\League of Legends\LeagueClient.exe')

def pingServers():
    currentPrefPing = config.getboolean('DEFAULT', 'analyticPingData')
    numberOfPings = config.getint('DEFAULT', 'numOfPings')
    if currentPrefPing == True:
        for i in range(numberOfPings):
            cmd = ['ping', '-n', '1', '104.160.142.3']
            try:
                output = subprocess.check_output(cmd)
                output = output.split()
                output = output[11]
                output = output[5:]
                list.insert(END, 'Your avarage ms in EUNE is: ' + str(output.decode('utf-8')))
                root.update()
            except subprocess.CalledProcessError as e:
                list.insert(END, 'Error: Couldnt reach server')
                root.update()
        for i in range(numberOfPings):
            cmd = ['ping', '-n', '1', '104.160.141.3']
            try:
                output = subprocess.check_output(cmd)
                output = output.split()
                output = output[11]
                output = output[5:]
                list.insert(END, 'Your avarage ms in EUW is: ' + str(output.decode('utf-8')))
                root.update()
            except subprocess.CalledProcessError as e:
                list.insert(END, 'Error: Couldnt reach server')
                root.update()
    else:
        response_listEUNE = ping('104.160.142.3', size=40, count=numberOfPings)
        response_listEUW = ping('104.160.141.3', size=40, count=numberOfPings)
        list.insert(END, 'Your avarage ms in EUNE is: ' + str(response_listEUNE.rtt_avg_ms) + '\n')
        list.insert(END, 'Your avarage ms in EUW is: ' + str(response_listEUW.rtt_avg_ms) + '\n')

def openSettings():
    settingsWindow = tk.Toplevel(root, height=500, width=400, bg='#19b9ff')
    settingsWindow.title('Settings')
    settingsWindow.grab_set()
    pingingFormatButton = tk.Button(settingsWindow, text='Pinging format', padx=10, pady=5,
                                    fg='white',bg='#263D42', command=pingFormatPopup).pack()
    pingNumPrefButton = tk.Button(settingsWindow, text='Ping settings', padx=10, pady=5,
                                 fg='white', bg='#263D42', command=pingNumPrefPopup).pack()
    clientPrefButton = tk.Button(settingsWindow, text='Client preferences', padx=10, pady=5,
                                 fg='white', bg='#263D42', command=clientPrefPupup).pack()
    settingsWindow.grab_release()

def pingNumPrefPopup():
    popup = tk.Toplevel(root)
    numberOfPings = config.getint('DEFAULT', 'numOfPings')
    popup.grab_set()
    tk.Label(popup, text='How many pings do you want the program to perform?(Default is 4)', padx=20).pack()
    clicked = StringVar()
    clicked.set(str(numberOfPings))
    drop = OptionMenu(popup, clicked, '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12').pack()
    saveButton = tk.Button(popup, text='Save option', anchor='se',
                           fg='white', bg='#263D42', command=lambda: saveChangesInt(clicked.get(), 'numofpings')).pack()
    popup.grab_release()

def pingFormatPopup():
    popup = tk.Toplevel(root)
    v = tk.IntVar()
    popup.grab_set()
    tk.Label(popup, text='Do you prefer ping data to be extensive?', padx=20).pack()
    tk.Radiobutton(popup, text='Yes', padx=20, variable=v, value=1).pack()
    tk.Radiobutton(popup, text='No', padx=20, variable=v, value=2).pack()
    saveButton = tk.Button(popup, text='Save option', anchor='se',
                           fg='white', bg='#263D42', command=lambda: saveChangesFlag(v.get(), 'analyticPingData')).pack()
    popup.grab_release()

def clientPrefPupup():
    popup = tk.Toplevel(root)
    v = tk.IntVar()
    popup.grab_set()
    tk.Label(popup, text='Do you want your game to open when you run the program?', padx=20).pack()
    tk.Radiobutton(popup, text='Yes', padx=20, variable=v, value=1).pack()
    tk.Radiobutton(popup, text='No', padx=20, variable=v, value=2).pack()
    saveButton = tk.Button(popup, text='Save option', anchor='se',
                           fg='white', bg='#263D42', command=lambda: saveChangesFlag(v.get(), 'openClient')).pack()
    popup.grab_release()

def saveChangesInt(v, val):
    config.read(r'test.ini')
    config.set('DEFAULT', val, str(v))
    with open(r'test.ini', 'w') as configfile:
        config.write(configfile)
    popupmsg()

def saveChangesFlag(v, val):
    if v == 1:
        answer = True
    else:
        answer = False
    config.read(r'test.ini')
    config.set('DEFAULT', val, str(answer))
    with open(r'test.ini', 'w') as configfile:
        config.write(configfile)
    popupmsg()

def popupmsg():
    popupms = tk.Toplevel()
    popupms.title("!")
    label = tk.Label(popupms, text='Preference updated successfully', font=("Times", "24"))
    label.pack(side="top", fill="x", pady=10)
    popupms.after(1000, lambda: popupms.destroy())
    popupms.mainloop()

root = tk.Tk()
root.title('Ping Tester')

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
list = Listbox(root, yscrollcommand=scrollbar.set, height=30, width=40, font=('Courier', 20))
list.pack(side=LEFT, fill=BOTH)
scrollbar.config(command = list.yview)

pingServersButton = tk.Button(root, text='Ping Servers', padx=10, pady=5,
                              fg='white', bg='#263D42', command=pingServers).pack()
settingsButton = tk.Button(root, text='Settings', padx=10,
                           pady=5, fg='white', bg='#263D42', command=openSettings).pack()

root.mainloop()
