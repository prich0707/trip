import os
import tkinter as tk
from PIL import Image, ImageTk

def main():
    root = tk.Tk()
    root.title("여행가자 - 대한민국 지도")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, "map.jpg")

    map_img = Image.open(img_path)
    orig_w, orig_h = map_img.size  

    root.geometry(f"{orig_w}x{orig_h}")
    root.resizable(False, False)  

    map_photo = ImageTk.PhotoImage(map_img)
    lbl = tk.Label(root, image=map_photo)
    lbl.image = map_photo
    lbl.pack()

    root.mainloop()

if __name__ == "__main__":
    main()

