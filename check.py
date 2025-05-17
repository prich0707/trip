import os
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

# 전역으로 현재 열려 있는 Toplevel 창을 저장
current_win = None

# 1) 시·도별 RGB 범위
region_ranges = {
    "서울특별시":       {"r": (170, 216), "g": (186, 227), "b": (25,  99)},
    "인천광역시":       {"r": (156, 174), "g": (174, 199), "b": (107, 125)},
    "세종특별자치시":   {"r": (36,  50),  "g": (108, 125), "b": (74,  90)},
    "대전광역시":       {"r": (47,  70),  "g": (137, 153), "b": (95,  111)},
    "충청남도":         {"r": (73,  146), "g": (172, 224), "b": (125, 185)},
    "대구광역시":       {"r": (13,  116), "g": (83,  173), "b": (101, 185)},
    "부산광역시":       {"r": (196, 223), "g": (85,  128), "b": (109, 144)},
    "전라북도":         {"r": (233, 242), "g": (185, 191), "b": (26,  45)},
    "광주광역시":       {"r": (171, 234), "g": (111, 150), "b": (59,  90)},
    "경기도":           {"r": (198, 200), "g": (216, 219), "b": (30,  39)},
    "강원도":           {"r": (124, 124), "g": (188, 188), "b": (39,  39)},
    "충청북도":         {"r": (117, 123), "g": (192, 195), "b": (131, 144)},
    "경상북도":         {"r": (55,  55),  "g": (139, 139), "b": (175, 175)},
    "울산광역시":       {"r": (51,  59),  "g": (100, 107), "b": (230, 253)},
    "경상남도":         {"r": (213, 243), "g": (125, 131), "b": (137, 143)},
    "전라남도":         {"r": (236, 247), "g": (140, 147), "b": (76,  84)},
    "제주특별자치도":   {"r": (178, 187), "g": (122, 130), "b": (168, 183)},
}

# 2) 대구광역시 좌표 범위 (x_min, x_max, y_min, y_max)
region_bounds = {
    "대구광역시": {"x": (419, 461), "y": (372, 446)},
}

def find_region(x, y, r, g, b):
    # 1) 먼저 좌표+색상 검사
    for region, bounds in region_bounds.items():
        xmin, xmax = bounds["x"]
        ymin, ymax = bounds["y"]
        if xmin <= x <= xmax and ymin <= y <= ymax:
            rr = region_ranges[region]
            if rr["r"][0] <= r <= rr["r"][1] and rr["g"][0] <= g <= rr["g"][1] and rr["b"][0] <= b <= rr["b"][1]:
                return region
            return None
    # 2) 그 외는 색상만으로
    for region, rr in region_ranges.items():
        if region in region_bounds:
            continue
        if rr["r"][0] <= r <= rr["r"][1] and rr["g"][0] <= g <= rr["g"][1] and rr["b"][0] <= b <= rr["b"][1]:
            return region
    return None

# 3) 시·도별 추천 여행지 데이터
travel_spots = {
    "서울특별시":       ["경복궁", "남산타워", "북촌한옥마을"],
    "인천광역시":       ["송도 센트럴파크", "월미도", "차이나타운"],
    "세종특별자치시":   ["세종호수공원", "국립세종도서관", "고운뜰"],
    "대전광역시":       ["엑스포과학공원", "유성온천", "한밭수목원"],
    "충청남도":         ["공주 공산성", "부여 부소산", "태안 해변"],
    "대구광역시":       ["팔공산", "서문시장", "이월드"],
    "부산광역시":       ["해운대", "감천문화마을", "자갈치시장"],
    "전라북도":         ["전주 한옥마을", "전주 경기전", "덕진공원"],
    "광주광역시":       ["충장로", "무등산", "5·18기념공원"],
    "경기도":           ["수원화성", "남한산성", "에버랜드"],
    "강원도":           ["설악산", "강릉 경포대", "춘천 소양강"],
    "충청북도":         ["청주 상당산성", "단양 구경시장", "제천 의림지"],
    "경상북도":         ["경주 불국사", "안동 하회마을", "포항 영일대"],
    "울산광역시":       ["태화강 국가정원", "간절곶", "울산대공원"],
    "경상남도":         ["통영 한려수도", "거제도", "사천 비토섬"],
    "전라남도":         ["여수 밤바다", "순천만국가정원", "보성 녹차밭"],
    "제주특별자치도":   ["한라산", "성산일출봉", "협재해수욕장"],
}

# 4) 지도 이미지 로드
BASE    = os.path.dirname(os.path.abspath(__file__))
map_img = Image.open(os.path.join(BASE, "map.jpg"))
map_arr = np.array(map_img)

def open_region_window(region, master):
    global current_win
    # 1) 창이 없으면 생성 + 위치 고정
    if current_win is None or not current_win.winfo_exists():
        current_win = tk.Toplevel(master)
        current_win.title(f"{region} 추천 여행지")
        # 원하는 화면 위치로 고정
        current_win.geometry("+650+150")
    else:
        # 2) 창은 그대로, 내부 위젯만 제거
        for w in current_win.winfo_children():
            w.destroy()
        current_win.title(f"{region} 추천 여행지")

    # 3) 버튼 추가
    for spot in travel_spots.get(region, []):
        btn = tk.Button(current_win, text=spot,
                        command=lambda s=spot: print(f"선택된 여행지: {s}"))
        btn.pack(fill="x", padx=10, pady=5)

def on_click(event, master):
    x, y = event.x, event.y
    r, g, b = map_arr[y, x]
    region = find_region(x, y, r, g, b)
    if region:
        print(f"[DEBUG] 클릭된 지역: {region}")
        open_region_window(region, master)
    else:
        print(f"[DEBUG] 미확인 색상 또는 범위 밖: (x={x},y={y}) (R={r},G={g},B={b})")

def main():
    root = tk.Tk()
    root.title("여행가자 – 전국 시·도 판별 (고정 창)")

    canvas = tk.Canvas(root, width=map_img.width, height=map_img.height)
    canvas.pack()
    photo = ImageTk.PhotoImage(map_img)
    canvas.create_image(0, 0, anchor="nw", image=photo)

    canvas.bind("<Button-1>", lambda e: on_click(e, root))
    root.mainloop()

if __name__ == "__main__":
    main()
