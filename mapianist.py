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
    driver = webdriver.Chrome("/app/chromedriver", chrome_options=chrome_options)
    time.sleep(5)
    return driver


def crawling(EMAIL, PASSWORD):
    COMMENT = [
        '잘듣고갑니다~',
        '잘듣고가요~',
        '잘들었어요!',
        '피아노 잘 치시네요~',
        '너무 좋네요!',
        '대단하시네요',
        'wow!',
        '잘듣고갑니닷',
        '좋습니다앙',
        '좋아요~',
        '최고최고~',
        '좋네요~ㅎ',
        '잘봤어요~',
        '피아노 대박이네요!!!',
        '잘듣고가여',
        '와 멋지다',
        '피아노 느낌 대박 ㅎㅎ',
        '멋져요!',
        '잘들었어요~~~',
        '좋아요!',
        '잘 듣고 갑니다~',
        '좋은 음악 감사합니다~',
        '잘 들었어요 :)',
        '너무 좋아요!!',
    ]

    RANDOM = random.randrange(0, len(COMMENT) - 1)
    url = 'https://www.mapianist.com/main'
    try:
        driver = setup_chrome()
    except Exception as e:
        return 'none', e

    driver.get(url)
    time.sleep(10)

    driver.find_element_by_xpath('//*[@id="page-wrap"]/mapia-header/header/div/div[2]/a[1]').click()
    time.sleep(10)
    driver.find_element_by_name('mapiaEmail').send_keys(EMAIL)
    time.sleep(3)
    driver.find_element_by_name('password').send_keys(PASSWORD)
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/modal-container/div/div/mapia-login-modal/div[2]/form/button').click()
    time.sleep(10)

    if driver.page_source.find('sinersound') == -1:
        logger.info('login failed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    driver.find_element_by_xpath('//*[@id="page-wrap"]/mapia-main/div[2]/a[1]/div[1]/img').click()
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="write-page"]/div/div/div[3]/div/app-dailypoint/div/a').click()
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="blogList"]/div/div[2]/a[1]').click()
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="blog"]/div/article/header/h4')
    time.sleep(3)
    title = driver.title
    logger.info('%s' % title)
    time.sleep(2)
    logger.info('[%s] comment = %s' % (datetime.datetime.now().strftime('%y%m%d %T'), COMMENT[RANDOM]))
    driver.find_element_by_xpath('//*[@id="comment-area-0"]').send_keys(COMMENT[RANDOM])
    time.sleep(3)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="blog"]/div/mapia-post-comment/div[1]/form/button').send_keys("\n")
    time.sleep(10)
    url = driver.current_url
    driver.close()

    return url, COMMENT[RANDOM], title


if __name__=='__main__':
    envs = Env('/app/envs.txt')
    delay_time = random.randrange(0, 10800)
    now = datetime.datetime.now()
    logger.info('%s (delay: %s seconds)' % (now, delay_time))
    time.sleep(delay_time)
    try:
        url, comment, title = crawling(envs.data['MAPIA_EMAIL'], envs.data['MAPIA_PASSWORD'])
        slack_mapianist(url, comment, title)
    except Exception as e:
        slack_mapianist('none', str(e))