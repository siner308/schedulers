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
envs = Env('envs.txt').data

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
    logger.info(EMAIL + PASSWORD)
    try:
        driver = setup_chrome()
        logger.info('success init chromedriver')
    except Exception as e:
        return 'none', e
    url = 'https://www.youtube.com/feed/subscriptions'
    logger.info('entering url (%s)' % url)
    driver.get(url)
    time.sleep(10)
    logger.info('init envs')

    logger.info('send email')
    driver.find_element_by_name('Email').send_keys(EMAIL)
    time.sleep(5)
    logger.info('click email')
    driver.find_element_by_name('signIn').click()
    time.sleep(5)
    logger.info('send password')
    driver.find_element_by_name('Passwd').send_keys(PASSWORD)
    time.sleep(5)
    logger.info('summit')
    driver.find_element_by_name('signIn').click()
    time.sleep(10)
    logger.info('Am I success?')
    imgs = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer/div/ytd-grid-video-renderer/div/ytd-thumbnail/a/yt-img-shadow/img')
    posts = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer/div/ytd-grid-video-renderer/div/div[1]/div[1]/h3/a')
    authors = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-item-section-renderer[1]/div/ytd-shelf-renderer/div/div[2]/ytd-grid-renderer/div/ytd-grid-video-renderer/div/div[1]/div[1]/div/div[1]/div[1]/yt-formatted-string/a')
    logger.info('len = %s' % len(imgs))
    logger.info('len = %s' % len(posts))
    logger.info('len = %s' % len(authors))
    i = 0
    try:
        latest_post = subprocess.check_output("cat /data/crawler/youtube.latest", shell=True).decode('utf-8').split('\n')[0]
    except:
        latest_post = None
    for img, post, author in zip(imgs, posts, authors):
        img_src = img.get_attribute('src').split('?sqp')[0]
        title = post.text
        url = post.get_attribute('href').split('&t=')[0]
        logger.info(url)
        logger.info(latest_post)
        if i == 0:
            new_post = url
            subprocess.call("echo '%s' > /data/crawler/youtube.tmp" % url, shell=True)
            i += 1
        if url == latest_post:
            if i != 0:
                subprocess.call("rm /data/crawler/youtube.tmp", shell=True)
            break
        logger.info(title)
        author = author.text
        slack_youtube(url, title, author, img_src)
    subprocess.call("echo '%s' > /data/crawler/youtube.latest" % new_post, shell=True)


if __name__=='__main__':
    try:
        crawling(envs['GOOGLE_EMAIL'], envs['GOOGLE_PASSWORD'])
    except Exception as e:
        slack_youtube('none', str(e), '', '')
