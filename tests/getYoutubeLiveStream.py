import logging

import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def get_youtube_data():

    options = webdriver.ChromeOptions()

    youtube_url = "https://schedule.hololive.tv/lives"

    # 스케줄표를 기준으로 데이터를 작은 원형 케릭터로 출력

    # 창 숨기기
    options.add_argument("headless")

    # 프록시 사용
    PROXY_ADDRESS = "111.111.111.111:9999" # IP:Port #변경 필요

    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY_ADDRESS,
        "ftpProxy": PROXY_ADDRESS,
        "sslProxy": PROXY_ADDRESS,
        "proxyType": "MANUAL"
    }

    # 크롤링한 내용을 저장할 엑셀 파일 설정
    writer = pd.ExcelWriter('airpage.xlsx', engine='openpyxl')

    # 드라이버 설정 (드라이버가 있는 경로를 정확하게 지정 필요)
    browser = webdriver.Chrome("./chromedriver.exe", options=options)

    delay = 1
    browser.implicitly_wait(delay)

    target_url  = youtube_url + "/c/dlwlrma/featured" # iu

    browser.get(target_url)

    # 화면 크기 최대화
    browser.maximize_window()
    browser.implicitly_wait(delay)

    # 동영상 탭 클릭
    browser.implicitly_wait(delay)
    browser.find_element_by_xpath('//*[@id="tabsContent"]/tp-yt-paper-tab[2]').click()

    body = browser.find_element_by_tag_name('body')

    # 스크롤을 한참 내려서 (가능하면 큰 수) body 내용 확보하기
    scroll_count = 250
    while scroll_count:
        body.send_keys(Keys.PAGE_DOWN)
        browser.implicitly_wait(delay)
        scroll_count -= 1

    html0 = browser.page_source
    html = BeautifulSoup(html0,'html.parser')

    # 영상 목록 획득
    video_datas = html.find_all('ytd-grid-video-renderer',{'class':'style-scope ytd-grid-renderer'})

    video_url_list = []
    for i in range(len(video_datas)):
        url = youtube_url + video_datas[i].find('a',{'id':'thumbnail'})['href']
        video_url_list.append(url)

    dataframe = pd.DataFrame({ 'name':[], 'view_count':[], 'youtube_url':[], 'date':[], 'desc' : [] })


    for i in range(3):
        #for i in range(len(video_datas)):
        name = video_datas[i].find('a',{'id':'video-title'}).text
        url = youtube_url + video_datas[i].find('a',{'id':'thumbnail'})['href']
        for_view_count =video_datas[i].find('div',{'id':'metadata-line'})
        view_count = for_view_count.find_all('span',{'class':'style-scope ytd-grid-video-renderer'})[0].text.split()[1]

        cur_url = video_url_list[i]
        browser.get(cur_url)
        time.sleep(5)

        body = browser.find_element_by_tag_name('body')

        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(5)

        html0 = browser.page_source
        html = BeautifulSoup(html0,'html.parser')

        moreBtn = browser.find_element_by_xpath('//*[@class="more-button style-scope ytd-video-secondary-info-renderer"]')
        try:
            if moreBtn is not None:
                moreBtn.click()
        except:
            pass

        r_date = html.find('div',{'id':'info-strings'}).find('yt-formatted-string').text
        desc = html.find_all('yt-formatted-string',{'class' : 'content style-scope ytd-video-secondary-info-renderer'})[0].text
        insert_data = pd.DataFrame({ 'name':[name], 'view_count':[view_count], 'youtube_url':[url], 'date':[r_date], 'desc' : [desc] })
        # dataframe = dataframe.append(insert_data)
        # dataframe.to_excel(writer, index=False)
        # writer.save()
        print("Crawled : " + str(i))
        print("Crawled : " + insert_data)

    # writer.save()

get_youtube_data()