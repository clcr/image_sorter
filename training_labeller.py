"""Tiny gui prog for sorting images into one folder or another with keypresses"""

import argparse
import os
import tkinter as tk

from PIL import ImageTk, Image


def key_callback(event):
    print('ello')


class ImageSorter(tk.Frame):

    def get_next_file(self, event):
        print("Button pressed")
        self.current_image = ImageTk.PhotoImage(Image.open
                            (self.image_list[self.image_index]))
        self.image_panel = tk.Label(self, image = self.current_image)
        self.image_panel.pack()
        self.pack()

    def __init__(self, in_dir, true_dir, false_dir):
        super().__init__()
        self.in_dir_abs = os.path.abspath(in_dir)
        self.image_list = [os.path.join(self.in_dir_abs, image) for image
                        in os.listdir(in_dir) if image.endswith(".png")]

        print(self.image_list)

        self.image_index = 0
        self.current_image = ImageTk.PhotoImage(Image.open
                            (self.image_list[self.image_index]))
        self.image_panel = tk.Label(self, image = self.current_image)
        self.bind_class("<space>", key_callback)
        self.image_panel.pack()
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
