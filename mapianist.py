#-*- coding: utf-8 -*-

import random
import logging
import os
import datetime
import time
from selenium import webdriver
from logger import get_my_logger
from slack import slack_mapianist
from environments import Env

logger = get_my_logger('mapiacrawler')


def setup_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1280x900")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
#    driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
    driver = webdriver.Chrome("/app/chromedriver", chrome_options=chrome_options)
    time.sleep(5)
    return driver


def crawling(EMAIL, PASSWORD):
    COMMENT = [
        '멋진 연주 잘 듣고 갑니다!',
        '잘 듣고가요~',
        '잘 들었어요!',
        '피아노 잘 치시네요~',
        '오오..좋네요!',
        '대단하시네요',
        '피아노 선율이 좋네요 :)',
        '잘 듣고갑니닷!',
        '연주 잘 하시네요~',
        '멋진 연주네요~',
        '좋아요~',
        '잘 듣고가요!',
        '잘 듣고 갑니다~',
        '저도 연습해서 치고 싶은 연주예요!',
        '잘듣고갑니다',
        '잘들었어요~',
        '우와..멋져요~',
        '좋아요~',
        '잘 듣고가요~',
        '연주 잘 하시네요~ 대단하세요',
        '좋네요~',
        '잘 봤어요~',
        '대박이네요!',
        '잘 듣고 가요. 연주 잘 하시네요!',
        '오..멋져요!!',
        '느낌 좋아요ㅎㅎ',
        '멋져요!',
        '멋진 음악 감사합니다.',
        '좋아요!',
        '잘 듣고 갑니다~',
        '좋은 음악 감사합니다~',
        '잘 들었어요 :)',
        '너무 좋네요~',
    ]

    RANDOM = random.randrange(0, len(COMMENT) - 1)
    main_url = 'https://www.mapianist.com/main'
    try:
        driver = setup_chrome()
    except Exception as e:
        logger.info('chrome exception')
        return 'none', e, '고장났어!!!'
    logger.info(main_url)
    driver.get(main_url)
    time.sleep(10)

    # 로그인 페이지로 이동하는 버튼
    #driver.find_element_by_xpath('//*[@id="page-wrap"]/mapia-header/header/div/div[2]/a[1]').click()
    driver.find_element_by_xpath('//*[@id="page-wrap"]/mapia-header-v2/header/div/div[2]/a[3]').click()
    time.sleep(10)
    logger.info('로그인 눌렀음')
    # ID
    #driver.find_element_by_name('mapiaEmail').send_keys(EMAIL)
    driver.find_element_by_xpath('/html/body/modal-container/div/div/mapia-login-modal/div[2]/form/div[1]/mp-input-form/div[2]/input').send_keys(EMAIL)
    time.sleep(3)
    logger.info('아이디 입력했음')
    # PASSWORD
    #driver.find_element_by_name('password').send_keys(PASSWORD)
    driver.find_element_by_xpath('/html/body/modal-container/div/div/mapia-login-modal/div[2]/form/div[2]/mp-input-form/div[2]/input').send_keys(PASSWORD)
    time.sleep(3)
    logger.info('비밀번호 입력했음')
    # 로그인 버튼
    #driver.find_element_by_xpath('/html/body/modal-container/div/div/mapia-login-modal/div[2]/form/button').click()
    driver.find_element_by_xpath('/html/body/modal-container/div/div/mapia-login-modal/div[2]/form/button').click()
    time.sleep(10)
    logger.info('로그인 버튼 눌렀음')
    if driver.page_source.find('sinersound') == -1:
        logger.info('login failed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    video_url = 'https://www.mapianist.com/video'
    driver.get(video_url)
    time.sleep(5)
    logger.info(video_url)
    # 첫번째 게시글
    #driver.find_element_by_xpath('//*[@id="page-wrap"]/mapia-main/div[2]/a[1]/div[1]/img').click()
    driver.find_element_by_xpath('//*[@id="page-wrap"]/mp-post-video-browse/mapia-post-video-list/div/div[3]/a[1]').click()
    time.sleep(5)
    logger.info('첫번째 게시글 들어왔음')
#    driver.find_element_by_xpath('//*[@id="write-page"]/div/div/div[3]/div/app-dailypoint/div/a').click()
#    time.sleep(5)

#    driver.find_element_by_xpath('//*[@id="blogList"]/div/div[3]/a[1]').click()
#    time.sleep(5)

#    driver.find_element_by_xpath('//*[@id="blog"]/div/article/header/h4')
#    time.sleep(3)
    title = driver.title
    logger.info('%s' % title)
    time.sleep(2)
    logger.info('[%s] comment = %s' % (datetime.datetime.now().strftime('%y%m%d %T'), COMMENT[RANDOM]))
    logger.info(title)
    # 댓글 입력창
#    driver.find_element_by_xpath('//*[@id="comment-area-0"]').send_keys(COMMENT[RANDOM])
    driver.find_element_by_xpath('//*[@id="comment-area-0"]').send_keys(COMMENT[RANDOM])
    time.sleep(6)
    logger.info(COMMENT[RANDOM])
    # 댓글 작성
    #driver.find_element_by_xpath('//*[@id="blog"]/div/mapia-post-comment/div[1]/form/button').send_keys("\n")
    driver.find_element_by_xpath('//*[@id="blog"]/div/mp-post-comment/div/div[1]/form/div/button').send_keys("\n")
    time.sleep(10)
    logger.info('댓글 작성버튼 눌렀음')
    url = driver.current_url
    driver.close()
    logger.info(url)
    return url, COMMENT[RANDOM], title


if __name__=='__main__':
    envs = Env('/app/envs.txt')
    #envs = Env('./envs.txt')
    delay_time = random.randrange(0, 10800)
    now = datetime.datetime.now()
    logger.info('%s (delay: %s seconds)' % (now, delay_time))
    time.sleep(delay_time)
    try:
        url, comment, title = crawling(envs.data['MAPIA_EMAIL'], envs.data['MAPIA_PASSWORD'])
        slack_mapianist(url, comment, title)
    except Exception as e:
        slack_mapianist('none', str(e))
