import os
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

def main():
    # 1) 이미지 로드
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path   = os.path.join(script_dir, "map.jpg")
    map_img    = Image.open(img_path)
    map_arr    = np.array(map_img)  # RGB 배열

    # 2) Tkinter 윈도우 + 캔버스 설정
    root = tk.Tk()
    root.title("여행가자 - 색상 샘플링 모드")

    canvas = tk.Canvas(root,
                       width=map_img.width,
                       height=map_img.height)
    canvas.pack()

    photo = ImageTk.PhotoImage(map_img)
    canvas.create_image(0, 0, anchor="nw", image=photo)

    # 3) 클릭 이벤트: 색상 샘플링
    def on_click(event):
        x, y = event.x, event.y
        # numpy 배열은 [행(y), 열(x), 채널]
        r, g, b = map_arr[y, x]
        print(f"샘플 좌표 ({x}, {y}) → (R={r}, G={g}, B={b})")

    canvas.bind("<Button-1>", on_click)

    root.mainloop()

if __name__ == "__main__":
    main()
