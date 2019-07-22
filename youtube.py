#-*- coding: utf-8 -*-

import sys
import random
import logging
import os
import datetime
import time
import subprocess
from selenium import webdriver
from logger import get_my_logger
from slack import slack_youtube
from environments import Env

logger = get_my_logger('youtube')


def setup_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1280x900")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)
    time.sleep(5)
    return driver


def crawling(EMAIL, PASSWORD):
    try:
        driver = setup_chrome()
    except Exception as e:
        return 'none', e
    url = 'https://www.youtube.com/feed/subscriptions'
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_name('Email').send_keys(EMAIL)
    time.sleep(5)
    driver.find_element_by_name('signIn').click()
    time.sleep(5)
    driver.find_element_by_name('Passwd').send_keys(PASSWORD)
    time.sleep(5)
    driver.find_element_by_name('signIn').click()
    time.sleep(10)
    todays_posts = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer/div/ytd-grid-video-renderer/div/ytd-thumbnail/a/yt-img-shadow/img')
    time.sleep(5)
    cnt_total = len(todays_posts)
    logger.info('len = %s' % cnt_total)
    try:
        latest_post = subprocess.check_output("cat /data/crawler/youtube.latest", shell=True).decode('utf-8').split('\n')[0]
        logger.info('latest post = (%s)' % latest_post)
    except:
        latest_post = None
    if cnt_total == 0:
        logger.info('there is no new posts')
        return
    i = 0 
    for cnt in range(1, cnt_total):
        img = driver.find_element_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer[1]/div/ytd-grid-video-renderer[%s]/div/ytd-thumbnail/a/yt-img-shadow/img' % cnt)
        post = driver.find_element_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer[1]/div/ytd-grid-video-renderer[%s]/div/div[1]/div[1]/h3/a' % cnt)
        author = driver.find_element_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer[1]/div/ytd-grid-video-renderer[%s]/div/div[1]/div[1]/div/div[1]/div[1]/yt-formatted-string/a' % cnt)
        try:
            img_src = img.get_attribute('src')
            time.sleep(3)
            logger.info('img_src = %s' % img_src)
            img_src = img_src.split('?sqp')[0]
        except:
            logger.error('failed to get attribute img_src')
        try:
            title = post.text
            time.sleep(3)
            logger.info('post = %s' % post)
        except:
            logger.error('failed to get title')
        try:
            author_name = author.text
            time.sleep(3)
            logger.info('author = %s' % author_name)
        except:
            logger.error('failed to get author')
        logger.info('title = %s\n author = %s' % (title, author_name))
        href = post.get_attribute('href')
        time.sleep(3)
        try:
            href = href.split('&t=')[0]
        except:
            pass
        logger.info('href = %s' % href)
        if i == 0:
            logger.info('latest url = %s' % href)
            new_post = href
            subprocess.call("echo '%s' > /data/crawler/youtube.tmp" % href, shell=True)
            i += 1
            logger.info('first post')
        logger.info('latest = %s' % latest_post)
        logger.info('newest = %s' % href)
        if href == latest_post:
            logger.info('latest post')
            break
        logger.info('[%s] %s' % (author_name, title))
        driver.find_element_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer/div/ytd-grid-video-renderer[%s]/div/div[1]/div[1]/h3/a' % cnt).click()
        time.sleep(10)
        youtuber_icon = driver.find_element_by_xpath('//*[@id="top-row"]/ytd-video-owner-renderer/a/yt-img-shadow/img')
        time.sleep(5)
        icon_url = youtuber_icon.get_attribute('src')
        logger.info('get icon url (%s)' % icon_url)
        slack_youtube(href, title, author_name, img_src, icon_url)
        logger.info('get %s' % url)
        driver.get(url)
        time.sleep(10)
    try:
        logger.info('trying update youtube.latest')
        subprocess.call("echo '%s' > /data/crawler/youtube.latest" % new_post, shell=True)
        logger.info('update youtube.latest')
    except Exception as e:
        logger.error('failed to update youtube.latest (%s)' % e)
    try:
        logger.info('trying update youtube.tmp')
        subprocess.call("rm /data/crawler/youtube.tmp", shell=True)
        logger.info('update youtube.tmp')
    except Exception as e:
        logger.error('failed to remove youtube.tmp (%s)' % e)

    driver.close()


if __name__=='__main__':
    envs = Env('/app/envs.txt')
    try:
        crawling(envs.data['GOOGLE_EMAIL'], envs.data['GOOGLE_PASSWORD'])
    except Exception as e:
        logger.exception('crawling crashed')
        slack_youtube('none', str(e), '', '', '')
