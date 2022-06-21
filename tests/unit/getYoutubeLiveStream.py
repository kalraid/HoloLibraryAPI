import platform
from collections import defaultdict
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy.orm import scoped_session

from app.database import get_session
from app.model import HoloMember

db_session = get_session()


def get_youtube_data():
    start = time.time()  # 시작 시간 저장

    options = webdriver.ChromeOptions()

    site_url = "https://schedule.hololive.tv/lives"

    # 스케줄표를 기준으로 데이터를 작은 원형 케릭터로 출력

    # 창 숨기기
    # options.add_argument("headless")

    # 프록시 사용
    PROXY_ADDRESS = "111.111.111.111:9999"  # IP:Port #변경 필요

    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY_ADDRESS,
        "ftpProxy": PROXY_ADDRESS,
        "sslProxy": PROXY_ADDRESS,
        "proxyType": "MANUAL"
    }

    # 크롤링한 내용을 저장할 엑셀 파일 설정
    writer = pd.ExcelWriter('airpage.xlsx', engine='openpyxl')

    # 드라이버 설정 (드라이버가 있는 경로를 정확하게 지정 필요)
    if platform.platform() == 'Linux':
        fileName = "../../resources/driver/chromedriver"
    else:
        fileName = "../../resources/driver/chromedriver.exe"

    browser = webdriver.Chrome(fileName, options=options)
    delay = 5
    browser.implicitly_wait(delay)

    target_url = site_url

    browser.get(target_url)

    # 화면 크기 최대화
    browser.maximize_window()
    browser.implicitly_wait(delay)

    # $('main >> .container').find('a') -> for -> href (주소),
    tab_content = browser.find_elements_by_class_name('tab-pane')[0]
    containers = tab_content.find_elements_by_xpath("./child::*")
    date_list = []
    schedule_date = ''

    alinks = []
    for i in containers:
        children = i.find_elements_by_xpath("./child::*")
        for row in children:
            navbar = row.find_elements_by_class_name('navbar')
            if navbar:
                schedule_date = navbar[0].text.split(' ')[0]

            for a in row.find_elements_by_tag_name('a'):
                data = defaultdict()
                split_data = a.text.split('\n')
                data['time'], data['name'], data['link'] = split_data[0], split_data[1], a.get_attribute('href')
                data['live'] = 'border: 3px solid red;' in i.get_attribute('style')
                data['date'] = schedule_date

                alinks.append(data)

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간  98초 약 2분 3~4분 마다 한번씩 돌면 될 듯
    print(alinks)

    save_youtube_live(alinks, db_session)

def save_youtube_live(live_links : list, db_session : scoped_session):
    for i in live_links:
        query = db_session.query(HoloMember)

        name = i.get('name')
        if 'a' <= name[0] <= "z" or 'A' <= name[0] <='Z': # name eng ( id or EN )
            name = name.lower()
            member = query.filter(HoloMember.member_name_eng.like('%'+name+'%')).one()
        else: # name is not english -> JP
            member = query.filter(HoloMember.member_name_jp.like('%'+name+'%')).one()

        pass


    pass

get_youtube_data()
