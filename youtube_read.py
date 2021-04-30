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
import urllib.request

root = tkinter.Tk()
WIDTH=900
HEIGHT=600
root.geometry(f"{WIDTH}x{HEIGHT}")
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
text_font = font.Font(family='Berlin Sans FB', size=16)
def get_api():
    global youtube
    api_key = "AIzaSyA210Ah9_sNyGhK5c6QfKpbf8J0AD1n_U8"
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube

def show_channels(event):
    global youtube,name_var,right_frame,top_frame
    search_key = name_var.get()
    #print(search_key)
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

    for a in right_frame.winfo_children():
        a.destroy()
    
    row=0
    column=0
    for title_key in channel_info.keys():
        c = Channel_list_icon(right_frame,title_key,channel_info[title_key],row,column)
        column = column+1
        if column==3:
            row=row+1
            column=0
        
    for a in top_frame.winfo_children():
        a.destroy()
    search_result_caption = Label(top_frame,text='Search Results',font=('Berlin Sans FB',28),bg='#fe0000',fg="#fcfcfa")
    search_result_caption.pack(side='left',padx=20,pady=10)

class Channel_list_icon:
    def __init__(self,rightframe,title,image_url,row,column):
        self.row = row
        self.column = column
        self.title = title
        self.image_url = image_url
        self.f = Frame(rightframe,width=150,height=150,bg='#fff')
        self.f.grid_propagate(0)
        self.download_user_image(self.image_url)
        self.channel_photo = ImageTk.PhotoImage(Image.open(f'profile_photo_{self.row}_{self.column}.jpg').resize((100,100)))  # PIL solution
        self.photo_label = Label(self.f,width=100, height=100,image=self.channel_photo,bg='#fff')  #relief=RAISED 
        self.photo_label.image = self.channel_photo
        self.title = Label(self.f,text=self.title,font=text_font,bg='#fff')
        self.display()
                           
    def download_user_image(self,URL):
        with urllib.request.urlopen(URL) as url:
            with open(f'profile_photo_{self.row}_{self.column}.jpg', 'wb') as f:
                f.write(url.read())            

    def display(self):
        #self.f.pack(side='left',padx=20,pady=20)
        self.f.grid(row=self.row,column=self.column,padx=25,pady=20)
        self.photo_label.grid(row=0,column=0)
        self.title.grid(row=1,column=0)
        
        
left_frame = Frame(root,width=200,height=600,bg='#fe0000')
left_frame.pack(side='left')
left_frame.pack_propagate(0)

photo = ImageTk.PhotoImage(Image.open("YouTube-Logo.jpg").resize((180,100)))  # PIL solution
label = Label(left_frame,width=180, height=100,image=photo,bg='#fe0000')  #relief=RAISED 
label.pack()


channel_name_lbl = Label(left_frame,text='Channel Name',font=text_font,bg='#fe0000',fg="#fcfcfa")
channel_name_lbl.pack()
name_var=tk.StringVar()
name_input_box = Entry(left_frame,width=30,textvariable=name_var)
name_input_box.bind('<Return>',show_channels)
name_input_box.pack()    

channel_id_lbl = Label(left_frame,text='Channel Id',font=text_font,bg='#fe0000',fg="#fcfcfa")
channel_id_lbl.pack(pady=(20,0))
id_input_box = Entry(left_frame,width=30)
id_input_box.pack()    

top_frame = Frame(root,width=WIDTH-200,height=80,bg='#fe0000')
top_frame.pack(side='top',expand=True,fill='x')
top_frame.pack_propagate(0)
search_result_caption = Label(top_frame,text='Search Results',font=('Berlin Sans FB',28),bg='#fe0000',fg="#fcfcfa")
search_result_caption.pack(side='left',padx=20,pady=10)

right_frame = Frame(root,width=WIDTH-200,height=520,bg='#fff')
right_frame.pack(side='bottom',expand=True,fill='both')
right_frame.pack_propagate(0)
root.mainloop()