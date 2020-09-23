import pyupbit
import requests
from bs4 import BeautifulSoup

def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    return BeautifulSoup(res.text, "lxml")

def print_news(title, link):
    title_text = "{}\n".format(title)
    link_text = "({})".format(link) + "\n"
    return title_text + link_text

def scrape_weather():
    # print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 비, 어제보다 1˚ 낮아요
    cast = soup.find("p", attrs={"class":"cast_txt"}).get_text()
    curr_temp = soup.find("p", attrs={"class":"info_temperature"}).get_text().replace("도씨", "")
    min_temp = soup.find("span", attrs={"class":"min"}) .get_text() # 최저온도
    max_temp = soup.find("span", attrs={"class":"max"}) .get_text() # 최고온도
    # 오전/오후 강수확률
    morning_rain_rate = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip()
    afternoon_rain_rate = soup.find("span", attrs={"class":"point_time afternoon"}).get_text().strip()
    # 미세먼지
    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text() # 미세먼지
    pm25 = dust.find_all("dd")[1].get_text() # 초미세먼지

    # 출력
    # print(cast)
    # print("현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp))
    # print("오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate))
    # print("미세먼지 {}".format(pm10))
    # print("초미세먼지 {}".format(pm25))
    # print()
    return "[오늘의 서울날씨]" + "\n" + cast + "\n" + "현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp) + "\n" + "오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate) + "\n" + "미세먼지 {}".format(pm10) + "\n" + "초미세먼지 {}".format(pm25) + "\n" + "\n"


def scrape_headline_news():
    txt = "[헤드라인 뉴스]" + "\n"
    # print("[헤드라인 뉴스]")
    url = "http://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
    for news in news_list:
        title = news.find("a").get_text().strip()
        link =  url + news.find("a")["href"]
        txt += print_news(title, link)
    return txt + "\n"



def scrape_coin_news():
    txt = "[뉴스]" + "\n"
    # print("[블록체인 뉴스]")
    url = "https://kr.coinness.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"newscontainer"}).find_all("li", limit=30)
    for news in news_list:
        content = news.find_all("a")[0]
        time = content.find("span", attrs={"class":"newstime"})
        if time:
            time = content.find("span", attrs={"class":"newstime"}).get_text().strip()
            title = "[{}] {}".format(time, content.find("h3").get_text().replace(time, "").strip())
            link =  url + content["href"]
            txt += print_news(title, link)
    return txt + "\n"


def scrape_coin_price():
    txt = "[시세]" + "\n"
    # BTC
    df_btc = pyupbit.get_ohlcv("KRW-BTC", "day", 10)
    btc = "{:,}".format(df_btc['close'][-1])
    btc_price = "BTC - {}원".format(btc.replace(".0", ""))
    txt += btc_price + "\n"

     # ETH
    df_eth = pyupbit.get_ohlcv("KRW-ETH", "day", 10)
    eth = "{:,}".format(df_eth['close'][-1])
    eth_price = "ETH - {}원".format(eth.replace(".0", ""))
    txt += eth_price + "\n"

    # ADA
    df_ada = pyupbit.get_ohlcv("KRW-ADA", "day", 10)
    ada = "{:,}".format(df_ada['close'][-1])
    ada_price = "ADA - {}원".format(ada.replace(".0", ""))
    txt += ada_price + "\n"

    return txt + "\n"