import time as t

import requests
import spotipy
from spotipy import Spotify, SpotifyOAuth
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import subprocess


def playing():
    try:
        tracks = spotify.currently_playing()
        if tracks is None:
            return False
        return tracks["is_playing"]
    except requests.exceptions.HTTPError:
        return False


def timer(sleep):
    # t.sleep(60 * sleep)

    if not playing():
        messagebox.showerror('Error: No Track Playing', 'Unable to detect any active track '
                                                        '\n(Spotify may not be open)')
    else:
        pause()


def pause():
    # print("timer finished, attempting pause")
    try:
        spotify.pause_playback(device_id=None)
        return True
    except spotipy.exceptions.SpotifyException:
        messagebox.showerror('Error: Unknown', '(May be caused by no device being open or no music being played)')
        return False


def get_token():
    auth_scope = "user-modify-playback-state user-read-currently-playing"
    # user = "uewhvcdjd4hlwtfxpsl1svyt0"
    client_id = "eb0ab2ef0ecc453ea6674b6fae96f63c"
    secret = "e3e1e59769024041b8467f4f77319303"
    url = "http://localhost:8080"
    auth = spotipy.SpotifyOAuth(
        client_id=client_id,
        client_secret=secret,
        scope=auth_scope,
        redirect_uri=url
    )
    return auth


def open_spotify(path):
    subprocess.Popen(path)


def custom_time(time):
    if validate_time(time):
        timer(int(time))


def validate_time(input_time):
    # integers only
    for char in input_time:
        if not char.isdigit():
            messagebox.showinfo('Custom Time', 'May only enter in integers')
            return False
    # no empty input
    if len(input_time) == 0:
        messagebox.showinfo('Custom Time', 'Field cannot be empty')
        return False
    # minimum value
    numeric_time = int(input_time)
    if numeric_time == 0:
        messagebox.showinfo('Custom Time', 'Must enter value greater than zero')
        return False
    elif numeric_time > 60:
        messagebox.showinfo('Custom Time', 'Max sleep timer is 60 minutes')
        return False

    return True


if __name__ == '__main__':
    spotify = spotipy.Spotify(auth_manager=get_token())

    root = Tk()
    root.title("Spotify Sleep Timer")
    root.geometry("850x300")

    defaultTimes = Label(root, text="Select a default time", font=("Arial", 18))
    customTimes = Label(root, text="Select a custom time ", font=("Arial", 18))

    defaultTimes.place(x=30, y=40)
    customTimes.place(x=30, y=100)

    defaultFifteen = Button(root, text="15 Minutes", font=("Arial", 16), command=lambda: timer(15))
    defaultTen = Button(root, text="10 Minutes", font=("Arial", 16), command=lambda: timer(10))
    defaultFive = Button(root, text="5 Minutes", font=("Arial", 16), command=lambda: timer(5))

    defaultFive.place(x=300, y=40)
    defaultTen.place(x=450, y=40)
    defaultFifteen.place(x=600, y=40)

    customTime = Entry(root)
    customSubmit = Button(root, text="Submit", font=("Arial", 15), command=lambda: custom_time(customTime.get()))

    customTime.place(x=300, y=100)
    customSubmit.place(x=450, y=100)

    root.mainloop()
