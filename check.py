import os
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

current_win = None

# 1) 시·도별 RGB 범위 (충청남도만 업데이트)
region_ranges = {
    "서울특별시":       {"r": (170, 216), "g": (186, 227), "b": (25,  99)},
    "인천광역시":       {"r": (156, 174), "g": (174, 199), "b": (107, 125)},
    "세종특별자치시":   {"r": (36,  50),  "g": (108, 125), "b": (74,  90)},
    "대전광역시":       {"r": (47,  70),  "g": (137, 153), "b": (95,  111)},
    "충청남도":         {"r": (67,  90),  "g": (178, 192), "b": (129, 145)},
    "대구광역시":       {"r": (11,   36), "g": (81,   102), "b": (98,  120)},
    "부산광역시":       {"r": (196, 223), "g": (85,  128), "b": (109, 144)},
    "전라북도":         {"r": (233, 242), "g": (185, 191), "b": (26,  45)},
    "광주광역시":       {"r": (171, 234), "g": (111, 150), "b": (59,  90)},
    "경기도":           {"r": (193, 208), "g": (213, 224), "b": (28,  48)},
    "강원도":           {"r": (124, 124), "g": (188, 188), "b": (39,  39)},
    "충청북도":         {"r": (119, 130), "g": (185, 203), "b": (128, 141)},
    "경상북도":         {"r": (49,   70),  "g": (133, 146), "b": (159, 182)},
    "울산광역시":       {"r": (51,   59),  "g": (100, 107), "b": (230, 253)},
    "경상남도":         {"r": (213, 243), "g": (125, 131), "b": (137, 143)},
    "전라남도":         {"r": (236, 247), "g": (140, 147), "b": (76,   84)},
    "제주특별자치도":   {"r": (178, 187), "g": (122, 130), "b": (168, 183)},
}

# 2) 좌표+색 검사용 박스: 서울, 경기도, 경상북도, 대구, 충청남도
region_bounds = {
    "서울특별시": [(268, 192, 292, 211)],
    "경기도":     [(255, 123, 355, 275)],
    "경상북도":   [(373, 275, 531, 444)],
    "대구광역시": [(431, 398, 453, 435)],
    "충청남도":   [(207, 277, 331, 385)],
}

# 3) 추천 여행지 데이터
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

# 4) 지도 로드 & OpenCV 변환
map_img = Image.open("map.jpg")
map_arr = np.array(map_img)
cv_img  = cv2.cvtColor(map_arr, cv2.COLOR_RGB2BGR)

def highlight_region(region):
    """region_bounds와 색상 범위로 마스크를 자른 뒤 하이라이트"""
    # 원본 그레이스케일 준비
    gray     = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # 색상 범위 마스크
    rr = region_ranges[region]
    lower = np.array([rr["b"][0], rr["g"][0], rr["r"][0]])
    upper = np.array([rr["b"][1], rr["g"][1], rr["r"][1]])
    mask0 = cv2.inRange(cv_img, lower, upper)

    # 박스 범위가 정의된 지역은 박스로 잘라내기
    if region in region_bounds:
        box_mask = np.zeros_like(mask0)
        for x1, y1, x2, y2 in region_bounds[region]:
            box_mask[y1:y2, x1:x2] = 255
        mask0 = cv2.bitwise_and(mask0, box_mask)

    # 컬러 + 그레이 배경 합성
    color = cv2.bitwise_and(cv_img, cv_img, mask=mask0)
    bg    = cv2.bitwise_and(gray_bgr, gray_bgr, mask=cv2.bitwise_not(mask0))
    comp  = cv2.add(color, bg)
    comp  = cv2.cvtColor(comp, cv2.COLOR_BGR2RGB)
    return Image.fromarray(comp)

def find_region(x, y, r, g, b):
    # 1) 박스 검사 → 2) 색상만 검사
    for region, boxes in region_bounds.items():
        for x1,y1,x2,y2 in boxes:
            if x1<=x<=x2 and y1<=y<=y2:
                if region in ("서울특별시","경기도"):
                    return region
                rr = region_ranges[region]
                if rr["r"][0]<=r<=rr["r"][1] and rr["g"][0]<=g<=rr["g"][1] and rr["b"][0]<=b<=rr["b"][1]:
                    return region
    for region,rr in region_ranges.items():
        if region in region_bounds: continue
        if rr["r"][0]<=r<=rr["r"][1] and rr["g"][0]<=g<=rr["g"][1] and rr["b"][0]<=b<=rr["b"][1]:
            return region
    return None

def open_region_window(region, master):
    global current_win
    if current_win and current_win.winfo_exists():
        for w in current_win.winfo_children():
            w.destroy()
    else:
        current_win = tk.Toplevel(master)
        current_win.geometry("+650+150")
    current_win.title(f"{region} 추천 여행지")
    for spot in travel_spots[region]:
        btn = tk.Button(current_win, text=spot,
                        command=lambda s=spot: print(f"선택된 여행지: {s}"))
        btn.pack(fill="x", padx=10, pady=5)

def on_click(event, master):
    global canvas, canvas_img_id
    x,y = event.x, event.y
    r,g,b = map_arr[y,x]
    region = find_region(x,y,r,g,b)
    if region:
        print(f"[DEBUG] 클릭된 지역: {region}")
        img2  = highlight_region(region)
        photo = ImageTk.PhotoImage(img2)
        canvas.image = photo
        canvas.itemconfig(canvas_img_id, image=photo)
        open_region_window(region, master)
    else:
        print(f"[DEBUG] 미확인 → (x={x},y={y}) (R={r},G={g},B={b})")

def main():
    global canvas, canvas_img_id
    root = tk.Tk()
    root.title("여행가자 – 하이라이트 모드")

    canvas = tk.Canvas(root, width=map_img.width, height=map_img.height)
    canvas.pack()
    photo = ImageTk.PhotoImage(map_img)
    canvas.image      = photo
    canvas_img_id     = canvas.create_image(0,0,anchor="nw",image=photo)
    canvas.bind("<Button-1>", lambda e: on_click(e, root))
    root.mainloop()

if __name__ == "__main__":
    main()
