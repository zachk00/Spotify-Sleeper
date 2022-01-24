import threading
import requests
import spotipy
from spotipy import Spotify, SpotifyOAuth
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from settings import Settings
from PIL import ImageTk, Image

root = Tk()
user_settings = Settings()


def playing():
    try:
        tracks = spotify.currently_playing()
        if tracks is None:
            return False
        return tracks["is_playing"]
    except requests.exceptions.HTTPError:
        return False


def timer_manager(sleep):
    # timer_check is obsolete, transition if playing to here
    stop = threading.Timer(sleep * 60, timer_check)
    stop.start()


def timer_check():
    if not playing():
        messagebox.showerror('Error: No Track Playing', 'Unable to detect any active track '
                                                        '\n(Spotify may not be open)')
    else:
        pause()


def pause():
    try:
        spotify.pause_playback(device_id=None)
        if user_settings.settings['close']:
            user_settings.close_spotify()
    except spotipy.exceptions.SpotifyException:
        messagebox.showerror('Error: Unknown', '(May be caused by no device being open or no music being played)')


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


def custom_time(time):
    if validate_time(time):
        timer_manager(int(time))


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

    if user_settings.settings['open']:
        user_settings.open_spotify()
    spotify = spotipy.Spotify(auth_manager=get_token())

    root_width = 850
    root_height = 300

    height_offset = int(root.winfo_screenheight() / 2) - int(root_height / 2)
    width_offset = int(root.winfo_screenwidth() / 2) - int(root_width / 2)

    root.title("Spotify Sleep Timer")
    root.geometry("{}x{}+{}+{}".format(root_width, root_height, width_offset, height_offset))

    defaultTimes = Label(root, text="Select a default time", font=("Arial", 18))
    customTimes = Label(root, text="Select a custom time ", font=("Arial", 18))

    defaultTimes.place(x=30, y=40)
    customTimes.place(x=30, y=100)

    defaultFifteen = Button(root, text="15 Minutes", font=("Arial", 16), command=lambda: timer_manager(15))
    defaultTen = Button(root, text="10 Minutes", font=("Arial", 16), command=lambda: timer_manager(10))
    defaultFive = Button(root, text="5 Minutes", font=("Arial", 16), command=lambda: timer_manager(5))

    defaultFive.place(x=300, y=40)
    defaultTen.place(x=450, y=40)
    defaultFifteen.place(x=600, y=40)

    customTime = Entry(root)
    customSubmit = Button(root, text="Submit", font=("Arial", 15), command=lambda: custom_time(customTime.get()))

    customTime.place(x=300, y=100)
    customSubmit.place(x=450, y=100)

    settings_icon = ImageTk.PhotoImage(Image.open("icons/settings.png").resize((25, 25)))
    settings_btn = Button(root, image=settings_icon,
                          command=lambda: user_settings.open_settings(root, user_settings.get_status()))

    settings_btn.place(x=800, y=20)

    root.mainloop()
