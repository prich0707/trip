<<<<<<< HEAD
# check.py

import os
import webbrowser
=======
import os
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
<<<<<<< HEAD
import datetime
import pandas as pd

from calendar_widget import CalendarFrame  # 달력 위젯
import weather                             # weather.py 모듈
import hotel                               # hotel.py (get_accommodations)

current_win = None

# ── 1) 시·도별 RGB 대략 범위 ────────────────────────────────────────────────
=======

current_win = None

# 1) 시·도별 RGB 범위 (충청남도만 업데이트)
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
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

<<<<<<< HEAD
# ── 2) 좌표 기반 예외 판별용 박스 ─────────────────────────────────────────────
=======
# 2) 좌표+색 검사용 박스: 서울, 경기도, 경상북도, 대구, 충청남도
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
region_bounds = {
    "서울특별시": [(268, 192, 292, 211)],
    "경기도":     [(255, 123, 355, 275)],
    "경상북도":   [(373, 275, 531, 444)],
    "대구광역시": [(431, 398, 453, 435)],
    "충청남도":   [(207, 277, 331, 385)],
}

<<<<<<< HEAD
# ── 3) 추천 여행지 이름 리스트 (URL 없이) ────────────────────────────────────
travel_spots = {
    "서울특별시": [
        "롯데월드타워&롯데월드몰",
        "잠실한강공원",
        "롯데월드 어드벤처",
        "한성백제박물관",
        "롯데월드 아쿠아리움",
        "광화문",
    ],
    "인천광역시": [
        "강화루지(강화씨사이드리조트)",
        "자월도 장골해변",
        "백령도 콩돌해변",
        "인천상륙작전기념관",
        "트라이보울",
        "송암미술관",
    ],
    "세종특별자치시": [
        "베어트리파크",
        "무궁화테마공원",
        "금이성",
        "국립조세박물관",
        "세종전통문화체험관",
        "우주측지관측센터",
    ],
    "대전광역시": [
        "대전 한화생명 볼파크",
        "식장산 문화공원(해돋이전망대)",
        "한밭수목원",
        "스몹 대전",
        "화폐박물관",
        "국립중앙과학관",
    ],
    "충청남도": [
        "삽교호(아산)",
        "독대섬",
        "죽도 (보령)",
        "천안박물관",
        "윤봉길의사기념관",
        "독립기념관",
    ],
    "충청북도": [
        "보강천미루나무숲",
        "청춘 패러",
        "우암산",
        "대한민국 꽃돌문화원",
        "청남대 대한민국 임시정부 기념관",
        "수소안전뮤지엄",
    ],
    "경기도": [
        "부천시민운동장",
        "마장호수 출렁다리",
        "부천식물원",
        "수원화성박물관",
        "백남준아트센터",
        "국립지도박물관",
    ],
    "강원도": [
        "DMZ 평화의길(통일전망대코스)",
        "영진해변",
        "낙산도립공원",
        "대포만세운동기념관",
        "강릉단오제전수교육관",
        "태백시 문화예술회관",
    ],
    "경상북도": [
        "송정자연휴양림",
        "주왕산국립공원",
        "경주국립공원",
        "칠곡호국평화기념관",
        "경상북도 산림과학박물관",
        "세계유교문화박물관",
    ],
    "대구광역시": [
        "팔공산 케이블카",
        "이월드",
        "동촌유원지",
        "수성아트피아",
        "국립대구박물관",
        "국립대구과학관",
    ],
    "울산광역시": [
        "진하해수욕장",
        "슬도",
        "과개안(너븐개) 해안",
        "웨일즈 판타지움",
        "울산과학관",
        "현대예술관",
    ],
    "부산광역시": [
        "청사포 해변",
        "부산 송도해수욕장",
        "광안리해수욕장",
        "씨라이프부산아쿠아리움",
        "국립부산과학관",
        "부산박물관",
    ],
    "전라북도": [
        "전주한옥레일바이크",
        "변산반도국립공원",
        "마이산도립공원",
        "고창고인돌박물관",
        "남원 백두대간전시관",
        "부안청자박물관",
    ],
    "전라남도": [
        "오동도 등대",
        "담양습지",
        "세방마을",
        "국립나주박물관",
        "호남호국기념관",
        "섬진강기차마을생태학습관",
    ],
    "경상남도": [
        "하동 코리아 짚와이어",
        "지리산국립공원(하동)",
        "거제도 해금강",
        "진주남강유등전시관",
        "박진전쟁기념관",
        "창녕생태곤충원",
    ],
    "제주특별자치도": [
        "용두암",
        "한라산",
        "천지연폭포",
        "아쿠아플라넷 제주",
        "제주특별자치도립미술관",
        "제주항공우주박물관",
    ],
    "광주광역시": [
        "백마능선 (무등산권 국가지질공원)",
        "시민의 숲 야영장",
        "광주호",
        "4·19 민주혁명역사관",
        "5·18기념문화센터",
        "국립광주과학관",
    ],
}

# ── 4) 지도 로드 & OpenCV 변환 ─────────────────────────────────────────────────
BASE    = os.path.dirname(os.path.abspath(__file__))
map_img = Image.open(os.path.join(BASE, "map.jpg"))
=======
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
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
map_arr = np.array(map_img)
cv_img  = cv2.cvtColor(map_arr, cv2.COLOR_RGB2BGR)

def highlight_region(region):
<<<<<<< HEAD
    """
    클릭된 region(예: '강원도')만 컬러, 나머지는 그레이스케일로 만든 PIL 이미지 반환
    """
    gray     = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    rr       = region_ranges[region]
=======
    """region_bounds와 색상 범위로 마스크를 자른 뒤 하이라이트"""
    # 원본 그레이스케일 준비
    gray     = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # 색상 범위 마스크
    rr = region_ranges[region]
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
    lower = np.array([rr["b"][0], rr["g"][0], rr["r"][0]])
    upper = np.array([rr["b"][1], rr["g"][1], rr["r"][1]])
    mask0 = cv2.inRange(cv_img, lower, upper)

<<<<<<< HEAD
    # 박스 영역이 정의된 지역이면 박스 부분만 허용
    if region in region_bounds:
        box_m = np.zeros_like(mask0)
        for (x1, y1, x2, y2) in region_bounds[region]:
            box_m[y1:y2, x1:x2] = 255
        mask0 = cv2.bitwise_and(mask0, box_m)

=======
    # 박스 범위가 정의된 지역은 박스로 잘라내기
    if region in region_bounds:
        box_mask = np.zeros_like(mask0)
        for x1, y1, x2, y2 in region_bounds[region]:
            box_mask[y1:y2, x1:x2] = 255
        mask0 = cv2.bitwise_and(mask0, box_mask)

    # 컬러 + 그레이 배경 합성
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
    color = cv2.bitwise_and(cv_img, cv_img, mask=mask0)
    bg    = cv2.bitwise_and(gray_bgr, gray_bgr, mask=cv2.bitwise_not(mask0))
    comp  = cv2.add(color, bg)
    comp  = cv2.cvtColor(comp, cv2.COLOR_BGR2RGB)
    return Image.fromarray(comp)

def find_region(x, y, r, g, b):
<<<<<<< HEAD
    """
    (x, y) 위치의 (r,g,b) 값을 보고 어느 시·도인지 반환
    """
    # ① 박스 기준 우선 판별
    for region, boxes in region_bounds.items():
        for x1, y1, x2, y2 in boxes:
            if x1 <= x <= x2 and y1 <= y <= y2:
                if region in ("서울특별시", "경기도"):
                    return region
                rr = region_ranges[region]
                if rr["r"][0] <= r <= rr["r"][1] and rr["g"][0] <= g <= rr["g"][1] and rr["b"][0] <= b <= rr["b"][1]:
                    return region

    # ② 박스 영역에 걸리지 않으면, 색상만으로 판별
    for region, rr in region_ranges.items():
        if region in region_bounds:
            continue
        if rr["r"][0] <= r <= rr["r"][1] and rr["g"][0] <= g <= rr["g"][1] and rr["b"][0] <= b <= rr["b"][1]:
            return region
    return None

# 시·도(“광주광역시” 등) → 날씨 API 호출에 넣어 줄 문자열(“광주” 등) 매핑
region_name_map = {
    "서울특별시":       "서울",
    "인천광역시":       "인천",
    "세종특별자치시":   "세종",
    "대전광역시":       "대전",
    "충청남도":         "충남",
    "대구광역시":       "대구",
    "부산광역시":       "부산",
    "전라북도":         "전북",
    "광주광역시":       "광주",
    "경기도":           "경기",
    "강원도":           "강원",
    "충청북도":         "충북",
    "경상북도":         "경북",
    "울산광역시":       "울산",
    "경상남도":         "경남",
    "전라남도":         "전남",
    "제주특별자치도":   "제주",
}

def open_region_window(region, master):
    global current_win
    selected_spot = None

    if current_win and current_win.winfo_exists():
        current_win.destroy()

    current_win = tk.Toplevel(master)
    current_win.geometry("1000x800+650+150")
    current_win.title(f"{region} 추천 여행지")

    # ── 상단: 지도/달력 ─────────────────────────
    top_frame   = tk.Frame(current_win); top_frame.pack(fill="x", padx=10, pady=10)
    left_frame  = tk.Frame(top_frame, width=500, height=500); left_frame.pack(side="left", padx=(0,10)); left_frame.pack_propagate(False)
    right_frame = tk.Frame(top_frame, width=500, height=500, bg="#f0f0f0", relief="sunken", borderwidth=1)
    right_frame.pack(side="left"); right_frame.pack_propagate(False)

    cal_frame = CalendarFrame(right_frame)
    cal_frame.pack(expand=True, fill="both", padx=5, pady=5)

    # ── 날씨 스크롤 ─────────────────────────────
    weather_canvas       = tk.Canvas(current_win, height=120)
    h_scroll             = tk.Scrollbar(current_win, orient="horizontal", command=weather_canvas.xview)
    weather_canvas.configure(xscrollcommand=h_scroll.set)
    weather_scroll_frame = tk.Frame(weather_canvas)
    weather_canvas.create_window((0,0), window=weather_scroll_frame, anchor="nw")
    weather_canvas.pack(fill="x", padx=20, pady=(0,10))
    h_scroll.pack(fill="x", padx=20)

    # ── (중요!) 날씨 출력 로직 그대로 여기 안에 복사해 주세요 ─────────
    def on_show_weather():
        sd, ed = cal_frame.get_selected_range()
        if not sd or not ed:
            for w in weather_scroll_frame.winfo_children(): w.destroy()
            tk.Label(weather_scroll_frame,
                     text="⚠️ 날짜 두 개 선택하세요.", fg="red").pack(side="left", padx=5)
            weather_canvas.configure(scrollregion=weather_canvas.bbox("all"))
            return
        rn = region_name_map.get(region)
        if not rn:
            for w in weather_scroll_frame.winfo_children(): w.destroy()
            tk.Label(weather_scroll_frame,
                     text=f"❌ '{region}' 지원 불가", fg="red").pack(side="left", padx=5)
            weather_canvas.configure(scrollregion=weather_canvas.bbox("all"))
            return
        for w in weather_scroll_frame.winfo_children(): w.destroy()
        today = datetime.datetime.now().date()
        days  = list(pd.date_range(start=sd, end=ed))
        for d0 in days:
            d     = d0.to_pydatetime()
            delta = (d.date() - today).days
            if delta < 0:
                txt = f"{d:%Y-%m-%d} 🔹 이미 지난 날짜"
            elif delta <= 4:
                txt = weather.get_short_term_forecast(d, rn)
            elif delta <= 10:
                txt = weather.get_mid_term_forecast(d, rn)
            else:
                txt = f"{d:%Y-%m-%d} 🔹 예보 불가 (10일 초과)"
            sub = tk.Frame(weather_scroll_frame, relief="groove", borderwidth=1, padx=5, pady=5)
            sub.pack(side="left", padx=5, pady=5)
            tk.Label(sub, text=txt, justify="left", anchor="nw",
                     font=("맑은 고딕",10)).pack()
        weather_canvas.update_idletasks()
        weather_canvas.configure(scrollregion=weather_canvas.bbox("all"))

    cal_frame.range_button.config(text="선택한 날씨 출력", command=on_show_weather)

    # ── 지도 이미지 ─────────────────────────────
    img2  = highlight_region(region)
    ph2   = ImageTk.PhotoImage(img2.resize((500,500)))
    img_label = tk.Label(left_frame, image=ph2)
    img_label.image = ph2
    img_label.pack(fill="both", expand=True)

    # ── 여행지 버튼 ─────────────────────────────
    spots         = travel_spots.get(region, [])
    indoor_spots  = spots[3:6]
    outdoor_spots = spots[:3]

    def on_travel_spot_click(btn, spot):
        nonlocal selected_spot
        for b in indoor_btns + outdoor_btns:
            b.config(bg="SystemButtonFace")
        btn.config(bg="gold")
        selected_spot = spot
        path = os.path.join(BASE, "imgfile", f"{spot}.jpg")
        if os.path.exists(path):
            im = Image.open(path).resize((500,500))
            ip = ImageTk.PhotoImage(im)
            img_label.config(image=ip); img_label.image = ip

    indoor_btns  = []
    outdoor_btns = []

    indoor_frame  = tk.Frame(current_win)
    indoor_frame.pack(fill="x", padx=20, pady=(5,2))
    tk.Label(indoor_frame, text="실내 : ", font=("맑은 고딕",10,"bold")).pack(side="left", padx=(10,5))
    for s in indoor_spots:
        b = tk.Button(indoor_frame, text=s, width=25)
        b.config(command=lambda b_ref=b, sp=s: on_travel_spot_click(b_ref, sp))
        b.pack(side="left", padx=5, pady=2)
        indoor_btns.append(b)

    outdoor_frame = tk.Frame(current_win)
    outdoor_frame.pack(fill="x", padx=20, pady=(2,10))
    tk.Label(outdoor_frame, text="야외 : ", font=("맑은 고딕",10,"bold")).pack(side="left", padx=(10,5))
    for s in outdoor_spots:
        b = tk.Button(outdoor_frame, text=s, width=25)
        b.config(command=lambda b_ref=b, sp=s: on_travel_spot_click(b_ref, sp))
        b.pack(side="left", padx=5, pady=2)
        outdoor_btns.append(b)

    # ── 숙소 보기 토글 ─────────────────────────────
    accom_state   = {"show": False}
    accom_buttons = []
    link_labels   = []
    btn_frame     = None
    link_frame    = None

    def show_accom_photo(info):
        path = info["image"]
        if os.path.exists(path):
            im = Image.open(path).resize((500,500))
            ip = ImageTk.PhotoImage(im)
            img_label.config(image=ip); img_label.image = ip

    def toggle_accommodations():
        nonlocal btn_frame, link_frame
        if not accom_state["show"]:
            cal_frame.pack_forget()
            indoor_frame.pack_forget()
            outdoor_frame.pack_forget()

            sd, ed = cal_frame.get_selected_range()
            if not sd or not ed:
                return

            keyword = selected_spot or region_name_map[region]
            hotels = hotel.get_accommodations(
                keyword,
                sd.strftime("%Y-%m-%d"),
                ed.strftime("%Y-%m-%d"),
                "2"
            )

            btn_frame = tk.Frame(current_win)
            btn_frame.pack(fill="x", padx=20, pady=(5,2))
            for info in hotels:
                hb = tk.Button(
                    btn_frame, text=info["name"], width=20,
                    command=lambda inf=info: show_accom_photo(inf)
                )
                hb.pack(side="left", padx=5, pady=5)
                accom_buttons.append(hb)

            link_frame = tk.Frame(current_win)
            link_frame.pack(fill="x", padx=20, pady=(0,10))
            lk = tk.Label(link_frame,
                          text=hotels[0]["url"],
                          fg="blue", cursor="hand2")
            lk.pack(side="left", padx=5)
            lk.bind("<Button-1>",
                    lambda e, url=hotels[0]["url"]: webbrowser.open(url))
            link_labels.append(lk)

            toggle_btn.config(text="관광지 보기")
            accom_state["show"] = True

        else:
            for b in accom_buttons: b.destroy()
            for l in link_labels:   l.destroy()
            btn_frame.destroy()
            link_frame.destroy()
            accom_buttons.clear()
            link_labels.clear()

            cal_frame.pack(expand=True, fill="both", padx=5, pady=5)
            indoor_frame.pack(fill="x", padx=20, pady=(5,2))
            outdoor_frame.pack(fill="x", padx=20, pady=(2,10))

            toggle_btn.config(text="숙소 보기")
            accom_state["show"] = False

    toggle_frame = tk.Frame(current_win)
    toggle_frame.pack(fill="x", padx=20, pady=(0,10))
    toggle_btn = tk.Button(
        toggle_frame,
        text="숙소 보기",
        command=toggle_accommodations
    )
    toggle_btn.pack(side="right", padx=5, pady=2)


def on_click(event, master):
    global canvas, canvas_img_id
    x,y   = event.x, event.y
    r,g,b = map_arr[y, x]
    region = find_region(x,y,r,g,b)
    if not region:
        return
    img2 = highlight_region(region)
    ph2 = ImageTk.PhotoImage(img2)
    canvas.image = ph2
    canvas.itemconfig(canvas_img_id, image=ph2)
    open_region_window(region, master)
=======
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
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12

def main():
    global canvas, canvas_img_id
    root = tk.Tk()
    root.title("여행가자 – 하이라이트 모드")

    canvas = tk.Canvas(root, width=map_img.width, height=map_img.height)
    canvas.pack()
<<<<<<< HEAD
    ph = ImageTk.PhotoImage(map_img)
    canvas.image      = ph
    canvas_img_id     = canvas.create_image(0,0,anchor="nw",image=ph)
    canvas.bind("<Button-1>", lambda e: on_click(e, root))

    root.mainloop()

if __name__ == "__main__":
    main()
=======
    photo = ImageTk.PhotoImage(map_img)
    canvas.image      = photo
    canvas_img_id     = canvas.create_image(0,0,anchor="nw",image=photo)
    canvas.bind("<Button-1>", lambda e: on_click(e, root))
    root.mainloop()

if __name__ == "__main__":
    main()
>>>>>>> f7cf7ebdce991d7b134bfcf56efc37fc55292c12
