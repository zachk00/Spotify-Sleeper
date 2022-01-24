from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *
import yaml
import subprocess
from os.path import exists


class Settings:

    def __init__(self):

        self.proc = None
        self.window = None
        self.win_open = False
        # Need to read these from config file

        if exists('user_settings.yaml'):
            stream = open('user_settings.yaml', 'r')
            self.settings = yaml.load(stream, Loader=yaml.SafeLoader)
            stream.close()
        else:
            self.settings = {'path': '\\', 'close': False, 'open': False}
            self.update_config()

        self.path = StringVar()
        self.open = IntVar()
        self.close = IntVar()

        if self.settings['open']:
            self.open.set(1)
        else:
            self.open.set(0)

        if self.settings['close']:
            self.close.set(1)
        else:
            self.close.set(0)

    def update_open(self):
        if self.open.get() == 1:
            self.settings['open'] = True
        else:
            self.settings['open'] = False

        self.update_config()

    def update_close(self):
        if self.close.get() == 1:
            self.settings['close'] = True
        else:
            self.settings['close'] = False

        self.update_config()

    def update_path(self):
        if self.path.get() == "" and not self.test_path(self.settings['path']):
            # if the path entry is empty and there is no working path
            messagebox.showerror("Error", 'No path was provided.\nHowever, either automatic open \n'
                                          'or close was requested')
            return False
        elif self.path.get() != "":
            # check the path
            if self.test_path(self.path.get()):
                # if valid path was provided, update the config file
                self.update_config()
                return True
            else:
                messagebox.showerror('Error', 'Invalid Spotify Path')
                return False

        return True

    def update_settings(self):
        successful = True

        if (self.open.get() == 1 and not self.settings['open']) or (self.open.get() == 0) and self.settings['open']:
            self.update_open()

        if (self.close.get() == 1 and not self.settings['close']) or (self.close.get() == 0) and self.settings['close']:
            self.update_close()

        # if auto open or close is enabled
        if self.settings['open'] or self.settings['close'] or self.path.get() != "":
            successful = self.update_path()

        if successful:
            self.close_settings()

    def update_config(self):
        with open('user_settings.yaml', 'w') as file:
            yaml.dump(self.settings, file)
            file.close()

    def get_settings(self):
        stream = open('user_settings.yaml', 'r')
        self.settings = yaml.load(stream, Loader=yaml.SafeLoader)
        stream.close()

    def update_status(self, new_status):
        self.win_open = new_status

    def close_settings(self):
        self.win_open = False
        self.window.destroy()

    def set_elements(self):

        allow_on = Checkbutton(self.window, variable=self.open,
                               text="Allow Sleeper to automatically turn on spotify",
                               onvalue=1, offvalue=0, )
        allow_on.place(x=30, y=30)

        allow_off = Checkbutton(self.window, variable=self.close,
                                text="Allow Sleeper to automatically turn off spotify on timer end")

        allow_off.place(x=30, y=50)

        path_label = Label(self.window, text="Path to Spotify Executable")
        path_label.place(x=30, y=80)

        path_entry = Entry(self.window, textvariable=self.path)
        path_entry.place(x=175, y=80)

        confirm_btn = Button(self.window, text="Confirm", command=self.update_settings)
        confirm_btn.place(x=30, y=150)

    def open_settings(self, root, is_open):
        if not is_open:
            settings_width = 425
            settings_height = 250

            x, y = (int(s) for s in root.geometry().split("+")[1:])

            x_offset = x + int(settings_width / 2)
            y_offset = y + int(settings_height / 2)

            self.window = Toplevel(root)
            self.window.geometry("{}x{}+{}+{}".format(settings_width, settings_height, x_offset, y_offset))
            self.window.title("Settings")
            self.win_open = True
            self.window.protocol("WM_DELETE_WINDOW", self.close_settings)
            self.set_elements()

        else:
            return False

    def open_spotify(self):
        self.proc = subprocess.Popen(self.settings['path'])

    def close_spotify(self):

        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()

    def get_status(self):
        return self.win_open

    # returns true if provided path works, false otherwise
    def test_path(self, test_path):
        try:
            self.settings['path'] = test_path
            self.open_spotify()
            self.close_spotify()
            return True
        except WindowsError as e:
            return False
