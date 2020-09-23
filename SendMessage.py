import time, win32con, win32api, win32gui
import Webscraping as WS
import schedule
from datetime import datetime

# 카톡창 이름(열려있는 상태, 최소화x, 창뒤에 숨어있는 비활성화 상태 가능)
kakao_opentalk_name = "블록체인정보"

# 채팅방에 메시지 전송
def kakao_sendtext(chatroom_name, text):
    ## 핸들 채팅방 찾기
    hwndMain = win32gui.FindWindow(None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx(hwndMain, None, "RichEdit50W", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwndEdit)


# 엔터
def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)


# 채팅방 열기
def open_chatroom(chatroom_name):
    # 채팅방 목록 검색하는 Edit (채팅방이 열려있지 않아도 전송 가능하기 위해)
    hwndkakao = win32gui.FindWindow(None, "카카오톡")
    hwndkakao_edit1 = win32gui.FindWindowEx(hwndkakao, None, "EVA_ChildWindow", None)
    hwndkakao_edit2_1 = win32gui.FindWindowEx(hwndkakao_edit1, None, "EVA_Window", None)
    hwndkakao_edit2_2 = win32gui.FindWindowEx(hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)
    hwndkakao_edit3 = win32gui.FindWindowEx(hwndkakao_edit2_2, None, "Edit", None)

    # Edit에 검색 - 입력되어있는 텍스트가 있어도 덮어쓰기
    win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
    time.sleep(1) # 안정성 위해 필요
    SendReturn(hwndkakao_edit3)
    time.sleep(1)


def Action():
    open_chatroom(kakao_opentalk_name)
    text = WS.scrape_coin_price() + WS.scrape_coin_news()
    kakao_sendtext(kakao_opentalk_name, text)
    print(datetime.today().strftime("%Y-%m-%d %H:%M:%S") + " 전송완료")

# 매일 8시에 실행
schedule.every().day.at("08:00").do(Action)
schedule.every().day.at("18:00").do(Action)

if __name__ == "__main__":
    print(" ================== KakaoTalk Bot 실행 ================== ")

    while True:
        schedule.run_pending()
        time.sleep(1)