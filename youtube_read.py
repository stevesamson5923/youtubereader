import tkinter
import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox, Scrollbar,Canvas
from tkinter import Menu, filedialog
from PIL import ImageTk, Image
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
import random
from apiclient.discovery import build

root = tkinter.Tk()
root.geometry("800x600")
root.resizable(0,0)
root.title("Library Management System")

main_menu_font = font.Font(family='Times New Roman', size=10, weight='bold')

############### MENUBAR 

menubar = Menu(root)  
file = Menu(menubar, tearoff=0)  
file.add_command(label="New")  
file.add_command(label="Open")  
file.add_command(label="Save")  
file.add_command(label="Save as...")  
file.add_command(label="Close")  
  
file.add_separator()  
  
file.add_command(label="Exit", command=root.destroy)  
  
menubar.add_cascade(label="File", menu=file) 
 
edit = Menu(menubar, tearoff=0)  
edit.add_command(label="Undo")  
edit.add_separator()    
edit.add_command(label="Cut")  
edit.add_command(label="Copy")  
edit.add_command(label="Paste")  
edit.add_command(label="Delete")  
edit.add_command(label="Select All")  
menubar.add_cascade(label="Edit", menu=edit)  

help = Menu(menubar, tearoff=0)  
help.add_command(label="About")  
menubar.add_cascade(label="Help", menu=help)  
  
root.config(menu=menubar)  

youtube = None

def get_api():
    global youtube
    api_key = "AIzaSyA210Ah9_sNyGhK5c6QfKpbf8J0AD1n_U8"
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube



def show_channels(event):
    global youtube,name_var
    search_key = name_var.get()
    print(search_key)
    if youtube is None:
        get_api()
    req = youtube.search().list(part='snippet',
                            q=search_key,
                            type='channel',
                            maxResults=9) 
    res = req.execute()
    items_list = res['items']
    channel_info={}
    for channel in items_list:
        channel_info[channel['snippet']['title']] = channel['snippet']['thumbnails']['default']['url']
    
    #contains title and channel thumbnail
    print(channel_info)


left_frame = Frame(root,width=200,height=600,bg='#fe0000')
left_frame.pack(side='left')
left_frame.pack_propagate(0)

photo = ImageTk.PhotoImage(Image.open("YouTube-Logo.jpg").resize((180,100)))  # PIL solution
label = Label(left_frame,width=180, height=100,image=photo,bg='#fe0000')  #relief=RAISED 
label.pack()

text_font = font.Font(family='Berlin Sans FB', size=16)
channel_name_lbl = Label(left_frame,text='Channel Name',font=text_font,bg='#fe0000',fg="#fcfcfa")
channel_name_lbl.pack()
name_var=tk.StringVar()
name_input_box = Entry(left_frame,width=30,textvariable=name_var)
name_input_box.bind('<Return>',show_channels)
name_input_box.pack()    

channel_id_lbl = Label(left_frame,text='Channel Id',font=text_font,bg='#fe0000',fg="#fcfcfa")
channel_id_lbl.pack(pady=(20,0))
id_input_box = Entry(left_frame,width=30)
id_input_box.bind('<Enter>')
id_input_box.pack()    

right_frame = Frame(root,width=600,height=600,bg='#fff')
right_frame.pack(side='left')
right_frame.pack_propagate(0)
root.mainloop()