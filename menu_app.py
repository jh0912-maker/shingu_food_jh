import tkinter as tk
from tkinter import messagebox
import urllib.request
import ssl
import datetime
import json
import os
from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# 설정 / configuration
# -----------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8707545343:AAGLSUsmxgr2irc7aaVxjqpNvN-JEq8Ysco')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '8400311014')

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍱 신구대 식단 알리미 (Today/Tomorrow)")
        self.root.geometry("450x650")
        
        # 🟢 스타일 설정
        self.root.configure(bg="#f8f9fa")
        
        # 🟢 상단 타이틀
        title_label = tk.Label(root, text="🏫 신구대학교 식단 확인", font=("Malgun Gothic", 18, "bold"), fg="#2c3e50", bg="#f8f9fa")
        title_label.pack(pady=20)
        
        # 🟢 버튼 프레임
        btn_frame = tk.Frame(root, bg="#f8f9fa")
        btn_frame.pack(pady=10)
        
        # 오늘 메뉴 버튼
        self.btn_today = tk.Button(btn_frame, text="📅 오늘 식단 확인", width=15, height=2,
                                  font=("Malgun Gothic", 10), bg="#007bff", fg="white", 
                                  command=lambda: self.load_menu(0))
        self.btn_today.grid(row=0, column=0, padx=10)
        
        # 내일 메뉴 버튼
        self.btn_tomorrow = tk.Button(btn_frame, text="➡️ 내일 식단 확인", width=15, height=2,
                                     font=("Malgun Gothic", 10), bg="#28a745", fg="white", 
                                     command=lambda: self.load_menu(1))
        self.btn_tomorrow.grid(row=0, column=1, padx=10)
        
        # 🟢 결과 출력 영역
        self.menu_text = tk.Text(root, height=20, width=50, font=("Malgun Gothic", 10), 
                                bg="white", relief="flat", padx=10, pady=10)
        self.menu_text.pack(pady=20, padx=20)
        
        # 🟢 하단 전송 알림
        self.status_label = tk.Label(root, text="버튼을 눌러 식단을 확인하세요.", font=("Malgun Gothic", 9), fg="#6c757d", bg="#f8f9fa")
        self.status_label.pack(pady=5)

    def load_menu(self, day_offset):
        """메뉴 데이터를 가져와서 화면에 표시하고 텔레그램으로 전송합니다."""
        target_date = datetime.datetime.now() + datetime.timedelta(days=day_offset)
        weekday = target_date.weekday()
        date_str = target_date.strftime("%Y-%m-%d")
        
        self.menu_text.delete(1.0, tk.END)
        self.menu_text.insert(tk.END, f"🔄 {date_str}의 식단을 불러오는 중...\n")
        self.root.update()
        
        # 주말 확인
        if weekday > 4:
            msg = f"📅 {date_str} ({['월','화','수','목','금','토','일'][weekday]})\n주말에는 식당을 운영하지 않습니다. ☀️"
            self.menu_text.delete(1.0, tk.END)
            self.menu_text.insert(tk.END, msg)
            return

        # 크롤링 또는 고정 데이터 구성 (여기선 교육용으로 수요일/목요일 고정 데이터 예시)
        # 실제 사이트 크롤링은 menu_crawler.py 로직을 그대로 사용 가능합니다.
        
        content_msg = f"📅 {date_str} ({['월','화','수','목','금','목','금'][weekday]}) 식단 안내\n\n"
        
        # 예시용 식단 데이터 (Wednesday / Thursday mock data - 실제 크롤링 연동 가능)
        if weekday == 2: # 수요일
            content_msg += "🍱 [교직원식당]\n• 오징어깻잎볶음, 소고기뭇국, 메밀전병구이 등\n\n"
            content_msg += "🍱 [학생식당(서관)]\n• 조식: 햄참치마요덮밥\n• 중식: 순살안동찜닭, 미트소스스파게티, 불닭크림떡볶이\n"
        elif weekday == 3: # 목요일
            content_msg += "🍱 [교직원식당]\n• 제육두부김치, 어묵탕, 소시지야채볶음 등\n\n"
            content_msg += "🍱 [학생식당(서관)]\n• 조식: 스팸마요덮밥\n• 중식: 돈까스정식, 된장찌개, 비빔국수\n"
        else:
            content_msg += "🍱 [식당 공통]\n• 해당 요일의 메뉴 정보를 가져오려면 홈페이지를 확인해 주세요.\n (현재 교육용 목업 데이터입니다.)\n"

        content_msg += "\n맛있게 드세요! 😋"
        
        # 1. 화면 출력
        self.menu_text.delete(1.0, tk.END)
        self.menu_text.insert(tk.END, content_msg)
        
        # 2. 텔레그램 전송
        success = self.send_telegram(content_msg)
        
        if success:
            self.status_label.config(text=f"✅ {date_str} 식단이 텔레그램으로 전송되었습니다!", fg="#28a745")
        else:
            self.status_label.config(text="❌ 텔레그램 전송에 실패했습니다.", fg="#dc3545")

    def send_telegram(self, message):
        """텔레그램으로 메시지 발송 (urllib 사용)"""
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as response:
                return True
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
