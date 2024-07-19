import os
import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import filedialog, messagebox
import pygame.mixer as mixer  # pip install pygame

# Initializing the mixer
mixer.init()

# Play, Stop, Load, and Pause & Resume functions
def play_song(song_name: StringVar, songs_list: Listbox, status: StringVar):
    song_name.set(songs_list.get(ACTIVE))
    mixer.music.load(songs_list.get(ACTIVE))
    mixer.music.play()
    status.set("Song PLAYING")

def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Song STOPPED")

def load(listbox):
    os.chdir(filedialog.askdirectory(title='Open a songs directory'))
    tracks = os.listdir()
    listbox.delete(0, END)  # Clear the current listbox
    for track in tracks:
        listbox.insert(END, track)

def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Song PAUSED")

def resume_song(status: StringVar):
    mixer.music.unpause()
    status.set("Song RESUMED")

def fetch_news(headlines_listbox):
    try:
        response = requests.get("https://www.bbc.com/news")
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.select('.gs-c-promo-heading__title')
        headlines_listbox.delete(0, END)  # Clear the current listbox
        for headline in headlines:
            headlines_listbox.insert(END, headline.get_text())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch news: {e}")

# Creating the master GUI
root = Tk()
root.geometry('900x500')
root.title('Music Player and News Scraper')
root.resizable(0, 0)
root.configure(bg='black')

# All StringVar variables
current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

# Frames
top_frame = Frame(root, bg='black', width=900, height=50)
top_frame.pack(side=TOP, fill=X)

middle_frame = Frame(root, bg='black', width=900, height=100)
middle_frame.pack(side=TOP, fill=X)

bottom_frame = Frame(root, bg='black', width=900, height=350)
bottom_frame.pack(side=TOP, fill=BOTH, expand=True)

# Playlist ListBox
playlist_frame = Frame(bottom_frame, bg='black')
playlist_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

playlist_lbl = Label(playlist_frame, text="Playlist", bg='black', fg='white', font=('Helvetica', 14))
playlist_lbl.pack(side=TOP)

playlist = Listbox(playlist_frame, font=('Helvetica', 11), selectbackground='Gold', bg='black', fg='white')
playlist.pack(side=LEFT, fill=Y)

scroll_bar = Scrollbar(playlist_frame, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=Y)
playlist.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=playlist.yview)

# News Headlines ListBox
news_frame = Frame(bottom_frame, bg='black')
news_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

news_lbl = Label(news_frame, text="News Headlines", bg='black', fg='white', font=('Helvetica', 14))
news_lbl.pack(side=TOP)

headlines_listbox = Listbox(news_frame, font=('Helvetica', 11), selectbackground='Gold', bg='black', fg='white')
headlines_listbox.pack(side=LEFT, fill=BOTH, expand=True)

news_scroll_bar = Scrollbar(news_frame, orient=VERTICAL)
news_scroll_bar.pack(side=RIGHT, fill=Y)
headlines_listbox.config(yscrollcommand=news_scroll_bar.set)
news_scroll_bar.config(command=headlines_listbox.yview)

# Top Frame Labels
Label(top_frame, text='Currently Playing:', bg='black', fg='white', font=('Times', 14, 'bold')).pack(side=LEFT, padx=10)
song_lbl = Label(top_frame, textvariable=current_song, bg='black', fg='gold', font=("Times", 14), width=40)
song_lbl.pack(side=LEFT, padx=10)

# Buttons in the middle frame
btn_style = {"bg": "white", "fg": "black", "font": ("Georgia", 13), "width": 10, "relief": "raised"}

pause_btn = Button(middle_frame, text='Pause', **btn_style, command=lambda: pause_song(song_status))
pause_btn.pack(side=LEFT, padx=10, pady=10)

stop_btn = Button(middle_frame, text='Stop', **btn_style, command=lambda: stop_song(song_status))
stop_btn.pack(side=LEFT, padx=10, pady=10)

play_btn = Button(middle_frame, text='Play', **btn_style, command=lambda: play_song(current_song, playlist, song_status))
play_btn.pack(side=LEFT, padx=10, pady=10)

resume_btn = Button(middle_frame, text='Resume', **btn_style, command=lambda: resume_song(song_status))
resume_btn.pack(side=LEFT, padx=10, pady=10)

# Load button without using btn_style for width
load_btn = Button(middle_frame, text='Load Directory', bg='white', fg='black', font=("Georgia", 13), relief='raised', width=15, command=lambda: load(playlist))
load_btn.pack(side=LEFT, padx=10, pady=10)

# Fetch News button
fetch_news_btn = Button(middle_frame, text='Fetch News', bg='white', fg='black', font=("Georgia", 13), relief='raised', width=15, command=lambda: fetch_news(headlines_listbox))
fetch_news_btn.pack(side=LEFT, padx=10, pady=10)

# Label at the bottom that displays the state of the music
status_lbl = Label(root, textvariable=song_status, bg='black', fg='white', font=('Times', 12), justify=LEFT)
status_lbl.pack(side=BOTTOM, fill=X, pady=5)

# Finalizing the GUI
root.update()
root.mainloop()
