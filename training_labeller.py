"""Tiny gui prog for sorting images into one folder or another with keypresses"""

import argparse
import os
import shutil
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

class ImageSorter(tk.Frame):

    def key_handler(self, event):
        print(event)
        if event.keysym == "Left":
            self.move_image_to_true()
            self.get_next_file()
        if event.keysym == "Right":
            self.move_image_to_false()
            self.get_next_file()

    def move_image_to_true(self):
        shutil.move(self.current_image_path, self.true_dir)

    def move_image_to_false(self):
        shutil.move(self.current_image_path, self.false_dir)

    def get_next_file(self):
        print("Button pressed")
        try:
            self.image_index += 1
            self.current_image_path = self.image_list[self.image_index]
            self.current_image = ImageTk.PhotoImage(Image.open
                                (self.current_image_path))
            self.image_panel["image"]= self.current_image
            self.pack()
        except IndexError:
            # If we've hit the end of the list, unbind the keypress and tell
            # the user
            self.bind_all("<Key>", None, add='')
            self.image_panel["image"]==None
            self.image_panel["text"]=="All images sorted!"
            self.popupmsg("All images sorted")


    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()


    def validate_dir(self, path):
        if os.path.isdir(path):
            return path
        else:
            raise FileNotFoundError("{} is not a directory".format(path))

    def __init__(self, in_dir, true_dir, false_dir):
        super().__init__()
        self.in_dir_abs = self.validate_dir(os.path.abspath(in_dir))
        self.true_dir = self.validate_dir(os.path.abspath(true_dir))
        self.false_dir = self.validate_dir(os.path.abspath(false_dir))
        self.image_list = [os.path.join(self.in_dir_abs, image) for image
                        in os.listdir(in_dir) if image.endswith(".png")]

        print(self.image_list)

        self.image_index = 0
        self.current_image_path = self.image_list[self.image_index]
        self.current_image = ImageTk.PhotoImage(Image.open
                            (self.current_image_path))
        self.image_panel = tk.Label(self, image = self.current_image)
        self.folder_label = tk.Label(self,
            text="In folder: {}\nLeft key    folder: {}\nRight key folder {}".format(
                                                self.in_dir_abs, self.true_dir, self.false_dir)
                                                )
        self.bind_all("<Key>", self.key_handler)
        self.image_panel.pack()
        self.folder_label.pack()
        self.pack()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "A quick tk powered window for sorting a"
                                    "directory into two folders")
    parser.add_argument("image_dir")
    parser.add_argument("dir_1")
    parser.add_argument("dir_2")
    args = parser.parse_args()
    main = ImageSorter(args.image_dir, args.dir_1, args.dir_2)
    main.mainloop()
