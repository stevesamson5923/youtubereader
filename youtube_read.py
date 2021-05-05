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
from tkinter import ttk
import webbrowser
import vlc
import pafy
import json
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle,os
from google.auth.transport.requests import Request


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

credentials = None
youtube = None
def get_credentials():
    global credentials,youtube
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube','https://www.googleapis.com/auth/youtube.force-ssl']

    credentials = None
    if os.path.exists("token.pickle"):
        print("Loading credentials from file...")
        with open("token.pickle","rb") as token:
            credentials = pickle.load(token)
    
    # if there are no valid credentials available, then either refresh the token or log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("refereshing access token")
            credentials.refresh(Request())
        else:
            print("Fetching new tokens")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080,prompt='consent',authorization_prompt_message='')
            
            with open('token.pickle','wb') as f:
                print("saving credentials for future use")
                pickle.dump(credentials,f)
                
    youtube = build('youtube', 'v3', credentials=credentials)

#get_credentials()

def show_videos(event):
    global rightframe,search_result_caption
    print('text: ',event.widget.get())
    search_text = event.widget.get()
    
    for a in right_frame.winfo_children():
        a.destroy()
         
    search_result_caption.config(text='Search Key: '+search_text)   

    api_key = "AIzaSyA210Ah9_sNyGhK5c6QfKpbf8J0AD1n_U8"  
    #https://www.googleapis.com/youtube/v3/search?part=snippet&q=avengers&maxResults=20&key=AIzaSyA210Ah9_sNyGhK5c6QfKpbf8J0AD1n_U8
    #https://www.googleapis.com/youtube/v3/videos?part=statistics&id=SLD9xzJ4oeU&key=AIzaSyA210Ah9_sNyGhK5c6QfKpbf8J0AD1n_U8
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_text}&maxResults=20&key={api_key}'
    #req = youtube.search().list(part='snippet',q=search_text,
    #                        type='videos',maxResults=20)
    res = urllib.request.urlopen(url)
    data = json.loads(res.read())
    videos = data["items"]
    
    scroll_f = ScrollableFrame(right_frame)
    scroll_f.pack(expand=True,fill='both')
    
    for video in videos:
        vid_id = video["id"]["videoId"]
        vid_title = video["snippet"]["title"]
        vid_image_url = video["snippet"]["thumbnails"]["default"]["url"]
        vid_url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={vid_id}&key={api_key}'
        vid_res = urllib.request.urlopen(vid_url)
        vid_stats = json.loads(vid_res.read())
        vid_likes = vid_stats["items"][0]["statistics"]["likeCount"]
        vid_dislikes = vid_stats["items"][0]["statistics"]["dislikeCount"]
        vid_views = vid_stats["items"][0]["statistics"]["viewCount"]
        
        f1 = Frame(scroll_f.scrollable_frame,width=WIDTH-200,height=130,bg='#fff')
        f1.pack_propagate(0)
        f1.pack(expand=True,fill='both',padx=20,pady=10)
        
        Video_item(f1,vid_title,vid_image_url,vid_likes,vid_dislikes,vid_views,vid_id)
        
def show_channels(event):
    global youtube,name_var,right_frame,top_frame,search_result_caption
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
    channel_id_list={}
    for channel in items_list:
        channel_info[channel['snippet']['title']] = channel['snippet']['thumbnails']['default']['url']
        channel_id_list[channel['snippet']['title']] = channel['id']['channelId']
        
    for a in right_frame.winfo_children():
        a.destroy()
    
    row=0
    column=0
    for title_key in channel_info.keys():
        cid = channel_id_list[title_key]
        c = Channel_list_icon(right_frame,title_key,channel_info[title_key],cid,row,column,search_result_caption,subcribers_count)
        column = column+1
        if column==3:
            row=row+1
            column=0
        
    #for a in top_frame.winfo_children():
    #    a.destroy()
    search_result_caption = Label(top_frame,text='Search Results: '+str(len(channel_info))+' Channels',font=('Berlin Sans FB',28),bg='#fe0000',fg="#fcfcfa")
    #search_result_caption.pack(side='left',padx=20,pady=10)


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,bg='#fff')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class Video_item:
    def __init__(self,frame,videotitle,thumbnail_url,like,dislike,views,video_id):
        self.frame = frame
        self.item_frame = Frame(self.frame,width=600,height=120,bg='#fff')
        self.item_frame.bind('<Enter>',self.changetextcolor)
        self.item_frame.bind('<Leave>',self.changebackcolor)
        self.title = videotitle
        self.thumbnail_url = thumbnail_url
        self.like = like
        self.dislike = dislike
        self.views = views
        self.vidid = video_id
        self.download_user_image(self.thumbnail_url)
        self.thumb_image = ImageTk.PhotoImage(Image.open(f'thumb_{self.vidid}.jpg').resize((100,80)))  # PIL solution
        self.photo_label = Label(self.item_frame,width=100, height=80,image=self.thumb_image,bg='#fff',cursor='hand2')  #relief=RAISED 
        self.photo_label.image = self.thumb_image
        self.photo_label.bind('<Button-1>',self.play_video)
        #self.photo_label.bind('<Enter>',self.changetextcolor)
        #self.photo_label.bind('<Leave>',self.changebackcolor)        
        
        self.title_lbl = Label(self.item_frame,text=self.title,font=("Verdana",12),bg='#fff',cursor='hand2')
        self.title_lbl.bind('<Button-1>',self.play_video)
        #self.title_lbl.bind('<Enter>',self.changetextcolor)
        #self.title_lbl.bind('<Leave>',self.changebackcolor)
        
        self.like_img = ImageTk.PhotoImage(Image.open('like.png').resize((15,15)))  # PIL solution
        self.like_photo_label = Label(self.item_frame,width=15, height=15,image=self.like_img,bg='#fff',cursor='hand2')  #relief=RAISED 
        self.like_photo_label.image = self.like_img  
        self.like_photo_label.bind('<Button-1>',self.like_video)
        self.like_count = Label(self.item_frame,text=self.like,font=('Times New Roman',8),bg='#fff')                         
                                        
        self.dislike_img = ImageTk.PhotoImage(Image.open('dislike.png').resize((15,15)))  # PIL solution
        self.dislike_photo_label = Label(self.item_frame,width=15, height=15,image=self.dislike_img,bg='#fff',cursor='hand2')  #relief=RAISED 
        self.dislike_photo_label.image = self.dislike_img  
        self.dislike_photo_label.bind('<Button-1>',self.dislike_video)
        self.dislike_count = Label(self.item_frame,text=self.dislike,font=('Times New Roman',8),bg='#fff')
        
        self.view_img = ImageTk.PhotoImage(Image.open('view.png').resize((15,15)))
        self.view_photo_label = Label(self.item_frame,width=15, height=15,image=self.view_img,bg='#fff')  #relief=RAISED 
        self.view_photo_label.image = self.view_img  
        self.view_count = Label(self.item_frame,text=self.views,font=('Times New Roman',8),bg='#fff')                         

        self.display()
   
    def like_video(self,event):
        if not credentials or credentials.expired:
            get_credentials()
        res = youtube.videos().getRating(id=self.vidid).execute()
        liked_disliked = res['items'][0]['rating']
        if liked_disliked == 'like':
            self.like_img = ImageTk.PhotoImage(Image.open('like.png').resize((15,15)))  # PIL solution
            self.like_photo_label.config(image=self.like_img)
            self.like_photo_label.image = self.like_img  
            youtube.videos().rate(rating='none', id=self.vidid).execute()
        elif liked_disliked == 'dislike':
            self.like_img = ImageTk.PhotoImage(Image.open('like_done.png').resize((15,15)))  # PIL solution
            self.like_photo_label.config(image=self.like_img)
            self.like_photo_label.image = self.like_img              
            self.dislike_img = ImageTk.PhotoImage(Image.open('dislike.png').resize((15,15)))  # PIL solution
            self.dislike_photo_label.config(image=self.dislike_img)
            self.dislike_photo_label.image = self.dislike_img            
            youtube.videos().rate(rating='like', id=self.vidid).execute()
        elif liked_disliked == 'none':
            self.like_img = ImageTk.PhotoImage(Image.open('like_done.png').resize((15,15)))  # PIL solution
            self.like_photo_label.config(image=self.like_img)
            self.like_photo_label.image = self.like_img  
            youtube.videos().rate(rating='like', id=self.vidid).execute()

    def dislike_video(self,event):
        if credentials.expired:
            get_credentials()
        res = youtube.videos().getRating(id=self.vidid).execute()
        liked_disliked = res['items'][0]['rating']
        if liked_disliked == 'like':
            self.like_img = ImageTk.PhotoImage(Image.open('like.png').resize((15,15)))  # PIL solution
            self.like_photo_label.config(image=self.like_img)
            self.like_photo_label.image = self.like_img              
            self.dislike_img = ImageTk.PhotoImage(Image.open('dislike_done.png').resize((15,15)))  # PIL solution
            self.dislike_photo_label.config(image=self.dislike_img)
            self.dislike_photo_label.image = self.dislike_img            
            youtube.videos().rate(rating='dislike', id=self.vidid).execute()
        elif liked_disliked == 'dislike':
            self.dislike_img = ImageTk.PhotoImage(Image.open('dislike.png').resize((15,15)))  # PIL solution
            self.dislike_photo_label.config(image=self.dislike_img)
            self.dislike_photo_label.image = self.dislike_img  
        elif liked_disliked == 'none':
            self.dislike_img = ImageTk.PhotoImage(Image.open('dislike_done.png').resize((15,15)))  # PIL solution
            self.dislike_photo_label.config(image=self.dislike_img)
            self.dislike_photo_label.image = self.dislike_img  
            youtube.videos().rate(rating='like', id=self.vidid).execute()
    
    def changetextcolor(self,event):
        self.title_lbl.config(font=("Verdana"))        
        self.title_lbl.config(bg='#fe0000')
        self.item_frame.config(bg='#fe0000')         
        self.photo_label.config(bg='#fe0000')
        self.like_photo_label.config(bg='#fe0000')
        self.like_count.config(bg='#fe0000')
        self.dislike_photo_label.config(bg='#fe0000')
        self.dislike_count.config(bg='#fe0000')
        self.view_photo_label.config(bg='#fe0000')
        self.view_count.config(bg='#fe0000')
                               
        self.title_lbl.config(fg='#fff')
        self.like_count.config(fg='#fff')
        self.dislike_count.config(fg='#fff')
        self.view_count.config(fg='#fff')
                              
    def changebackcolor(self,event):
        self.title_lbl.config(font=("Verdana"))        
        self.title_lbl.config(bg='#fff')
        self.item_frame.config(bg='#fff')         
        self.photo_label.config(bg='#fff')
        self.like_photo_label.config(bg='#fff')
        self.like_count.config(bg='#fff')
        self.dislike_photo_label.config(bg='#fff')
        self.dislike_count.config(bg='#fff')
        self.view_photo_label.config(bg='#fff')
        self.view_count.config(bg='#fff')
                               
        self.title_lbl.config(fg='#000')                               
        self.like_count.config(fg='#000')
        self.dislike_count.config(fg='#000')
        self.view_count.config(fg='#000')
        
    def play_video(self,event):
        url = f"https://www.youtube.com/watch?v={self.vidid}"
  
        # creating pafy object of the video
        video = pafy.new(url)
          
        # getting best stream
        best = video.getbest()
          
        # creating vlc media player object
        media = vlc.MediaPlayer(best.url)
          
        # start playing video
        media.play()
    
    def download_user_image(self,URL):
        with urllib.request.urlopen(URL) as url:
            with open(f'thumb_{self.vidid}.jpg','wb') as f:
                f.write(url.read())   
    
    def display(self):
        self.item_frame.pack(side='left',expand=True,fill='both')
        self.photo_label.grid(row=0,column=0,rowspan=2,padx=(20,0),pady=15)
        self.title_lbl.grid(row=0,column=1,columnspan=6,padx=5,pady=5)
        self.like_photo_label.grid(row=1,column=1,padx=5,pady=5,sticky='w')
        self.like_count.grid(row=1,column=2,padx=5,pady=5,sticky='w')
        self.dislike_photo_label.grid(row=1,column=3,padx=5,pady=5,sticky='w')
        self.dislike_count.grid(row=1,column=4,padx=5,pady=5,sticky='w')
        self.view_photo_label.grid(row=1,column=5,padx=5,pady=5,sticky='w')
        self.view_count.grid(row=1,column=6,padx=5,pady=5,sticky='w')

class Channel_list_icon:
    def __init__(self,rightframe,title,image_url,cid,row,column,search_result_caption,subcribers_count):
        self.search_result_caption = search_result_caption
        self.subcribers_count = subcribers_count
        #self.back_but_label = back_but_label
        self.rf = rightframe
        self.row = row
        self.column = column
        self.title_text = title
        self.cid = cid
        self.sub_count = 0
        self.image_url = image_url
        self.f = Frame(rightframe,width=150,height=150,bg='#fff',cursor='hand2')
        self.f.bind('<Enter>',self.onEnter)
        self.f.bind('<Leave>',self.onLeave)
        self.f.bind('<Button-1>',self.open_channel)
        self.f.grid_propagate(0)
        self.download_user_image(self.image_url)
        self.channel_photo = ImageTk.PhotoImage(Image.open(f'profile_photo_{self.row}_{self.column}.jpg').resize((80,80)))  # PIL solution
        self.photo_label = Label(self.f,width=80, height=80,image=self.channel_photo,bg='#fff')  #relief=RAISED 
        self.photo_label.image = self.channel_photo
        self.photo_label.bind('<Button-1>',self.open_channel)
        self.title = Label(self.f,text=self.title_text,font=text_font,bg='#fff')
        self.title.bind('<Button-1>',self.open_channel)
        self.display()
                           
    def download_user_image(self,URL):
        with urllib.request.urlopen(URL) as url:
            with open(f'profile_photo_{self.row}_{self.column}.jpg','wb') as f:
                f.write(url.read())            
    
    def onEnter(self,event):
        self.f.config(bg='#fe0000')
        self.title.config(bg='#fe0000')
        self.title.config(fg='#fff')
                      
    def onLeave(self,event):
        self.f.config(bg='#fff')
        self.title.config(bg='#fff')
        self.title.config(fg='#000')
     
    #def main_screen(self,event):
    #    for a in right_frame.winfo_children():
    #        a.destroy()
           
    def open_channel(self,event):
        for a in right_frame.winfo_children():
            a.destroy()
         
        self.search_result_caption.config(text='Channel name: '+self.title_text)   
        
        #back_but = ImageTk.PhotoImage(Image.open("back.png").resize((60,60)))
        #self.back_but_label.config(image=back_but)
        #self.back_but_label.image = back_but
        #self.back_but_label.bind('<Button-1>',self.main_screen)
        
        scroll_f = ScrollableFrame(self.rf)
        scroll_f.pack(expand=True,fill='both')
        
        #f1 = Frame(scroll_f.scrollable_frame,width=WIDTH-200,height=40,bg='#fff')
        videos_list = self.get_videos_list()
        
        for video in videos_list:
            f1 = Frame(scroll_f.scrollable_frame,width=WIDTH-200,height=130,bg='#fff')
            f1.pack_propagate(0)
            f1.pack(expand=True,fill='both',padx=20,pady=10)
            video_title = video['snippet']['title']
            thumbnail_url = video['snippet']['thumbnails']['default']['url']
            video_id = video['snippet']['resourceId']['videoId']
            video_info = youtube.videos().list(part="snippet,statistics",id=video_id).execute()
            total_views = video_info['items'][0]['statistics']['viewCount']
            total_likes = video_info['items'][0]['statistics']['likeCount']
            total_dislikes = video_info['items'][0]['statistics']['dislikeCount']
            
            Video_item(f1,video_title,thumbnail_url,total_likes,total_dislikes,total_views,video_id)            
        
    def get_videos_list(self):
        channel_info_res = youtube.channels().list(id=self.cid, 
                                  part='statistics,contentDetails').execute()
        self.sub_count = channel_info_res['items'][0]['statistics']['subscriberCount']
        
        self.subcribers_count.config(text='Subscriber Count: '+str(self.sub_count))
        
        playlist_id = channel_info_res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        playlist_info_res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=10).execute()
        videos = playlist_info_res['items']
        return videos           
                   
    def display(self):
        #self.f.pack(side='left',padx=20,pady=20)
        self.f.grid(row=self.row,column=self.column,padx=(30,10),pady=(20,5))
        self.photo_label.grid(row=0,column=0,padx=30,pady=10)
        self.title.grid(row=1,column=0,pady=10)
        

def open_youtube(event):
    webbrowser.open("https://www.youtube.com/")
    #urllib.request.urlopen("https://www.youtube.com/")

left_frame = Frame(root,width=200,height=600,bg='#fe0000')
left_frame.pack(side='left')
left_frame.pack_propagate(0)


#back_but_label =  Label(left_frame,width=60, height=60,bg='#fe0000') 
#back_but_label.pack(padx=30,pady=(30,0))
                        
photo = ImageTk.PhotoImage(Image.open("YouTube-Logo.jpg").resize((180,100)))  # PIL solution
label = Label(left_frame,width=180, height=100,image=photo,bg='#fe0000',cursor='hand2')  #relief=RAISED 
label.pack(pady=(50,0))
label.bind('<Button-1>',open_youtube)

channel_name_lbl = Label(left_frame,text='Channel Name',font=text_font,bg='#fe0000',fg="#fcfcfa")
channel_name_lbl.pack()
name_var=tk.StringVar()
name_input_box = Entry(left_frame,width=30,textvariable=name_var)
name_input_box.bind('<Return>',show_channels)
name_input_box.pack()    

channel_id_lbl = Label(left_frame,text='Search Videos',font=text_font,bg='#fe0000',fg="#fcfcfa")
channel_id_lbl.pack(pady=(20,0))
id_input_box = Entry(left_frame,width=30)
id_input_box.bind('<Return>',show_videos)
id_input_box.pack()    

top_frame = Frame(root,width=WIDTH-200,height=80,bg='#fe0000')
top_frame.pack(side='top',expand=True,fill='x')
top_frame.pack_propagate(0)
search_result_caption = Label(top_frame,text='Search Results',font=('Berlin Sans FB',28),bg='#fe0000',fg="#fcfcfa")
search_result_caption.pack(side='left',padx=20,pady=10)
subcribers_count = Label(top_frame,text='',font=('Berlin Sans FB',12),bg='#fe0000',fg="#fcfcfa")
subcribers_count.pack(side='right',padx=20,pady=20)

right_frame = Frame(root,width=WIDTH-200,height=520,bg='#fff')
right_frame.pack(side='bottom',expand=True,fill='both')
right_frame.pack_propagate(0)
root.mainloop()