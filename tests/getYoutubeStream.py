import logging

import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import platform


def get_youtube_data():
    try:
        before_video_size = 156
        channel_id = 'UC8rcEBzJSleTkf_-agPM20g'
        url_strs = get_crawling_youtube_list_to_url_strs(channel_id, before_video_size)
        items = get_youtube_data_by_url_strs(url_strs)
        save_youtube_data(items)

    except Exception:
        Exception.with_traceback()


def get_crawling_youtube_list_to_url_strs(channel_url, before_video_size):
    # channel_id to video_channel_url
    channel_url = '/channel/' + channel_url + '/videos'

    options = webdriver.ChromeOptions()
    youtube_url = "https://www.youtube.com"
    # widnow hide
    options.add_argument("headless")
    # 프록시 사용
    PROXY_ADDRESS = "111.111.111.111:9999"  # IP:Port #변경 필요
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY_ADDRESS,
        "ftpProxy": PROXY_ADDRESS,
        "sslProxy": PROXY_ADDRESS,
        "proxyType": "MANUAL"
    }
    # 크롤링한 내용을 저장할 엑셀 파일 설정
    # writer = pd.ExcelWriter('airpage.xlsx', engine='openpyxl')
    # 드라이버 설정 (드라이버가 있는 경로를 정확하게 지정 필요)
    if platform.platform() == 'Linux':
        fileName = "../resources/driver/chromedriver"
    else:
        fileName = "../resources/driver/chromedriver.exe"
    browser = webdriver.Chrome(fileName, options=options)
    delay = 1
    browser.implicitly_wait(delay)
    target_url = youtube_url + channel_url
    browser.get(target_url)
    # 화면 크기 최대화
    browser.maximize_window()
    browser.implicitly_wait(delay)

    # get body
    body = browser.find_element_by_tag_name('body')
    # before video size / youtube scroll pageup video count  + 3
    scroll_count = before_video_size // 30 + 3
    while scroll_count:
        body.send_keys(Keys.PAGE_DOWN)
        browser.implicitly_wait(delay)
        scroll_count -= 1


    html0 = browser.page_source
    html = BeautifulSoup(html0, 'html.parser')
    # 영상 목록 획득
    video_datas = html.find_all('ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})
    video_url_list = []
    for i in range(len(video_datas)):
        url = youtube_url + video_datas[i].find('a', {'id': 'thumbnail'})['href']
        video_url_list.append(url)

    # browser.close()
    return ','.join(video_url_list)


def get_youtube_data_by_url_strs(video_url_list):
    logging.info(video_url_list)
    pass


def save_youtube_data(items):
    pass



get_youtube_data()
