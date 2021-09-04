import logging
import requests
import json
from slacker import Slacker
#from settings import SLACK_CHANNEL_GOOGLE_HOME_MINI
from environments import Env
from logger import get_my_logger


envs = Env('/app/envs.txt')
token = envs.data['SLACK_TOKEN']
slack = Slacker(token)


'''
def slack_google_home_mini(result):
    channel = SLACK_CHANNEL_GOOGLE_HOME_MINI
    username = 'GoogleHomeMini'
    icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSvgAMRYdFDaOHkqCCtJjO5VTZiUau7P-cjzqJ3KvAh1BWztOMb'
    slack.chat.post_message(text=result, channel=channel, username=username, icon_url=icon_url)
'''

def slack_mapianist(url, comment, title=None):
    #envs = Env('./envs.txt')
    channel = envs.data['SLACK_CHANNEL_MAPIANIST']
    username = envs.data['SLACK_USERNAME_MAPIANIST']
    icon_url = envs.data['SLACK_ICON_URL_MAPIANIST']
    if url != 'none':
        attachments = [{
            'title': '확인하기',
            'title_link': url,
            'author_name': title,
            'fallback': '댓글 보냈어~',
            'text': comment,
            'color': '#009000',
        }]
    else:
        attachments = [{
            'title': '고장났어!!!',
            'fallback': '고장났어!!',
            'text': comment,
            'color': '#FF0000',
        }]

    slack.chat.post_message(text=None, channel=channel, username=username, attachments=attachments, icon_url=icon_url)

'''
def slack_youtube(url, title, author, img_src, icon_url):
    envs = Env('/app/envs.txt')
    token = envs.data['SLACK_TOKEN']
    channel = envs.data['SLACK_CHANNEL_YOUTUBE']
    username = envs.data['SLACK_USERNAME_YOUTUBE']
    if url != 'none':
        attachments = [{
            'title': title,
            'title_link': url,
            'text': url,
            'image_url': img_src,
            'fallback': title,
            'color': '#009000'
        }]
    else:
        attachments = [{
            'title': '고장났어!!!',
            'fallback': '고장났어!!',
            'text': title,
            'color': '#FF0000'
        }]

    data = {
        "channel": channel,
        'username': author,
        'icon_url': icon_url,
        "attachments": attachments
    }
    logging.info(img_src)
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer %s' % token
    }
#    slack = Slacker(token)
#    slack.chat.post_message(text=None, channel=channel, username=author, attachments=attachments, icon_url=icon_url)
    url = 'https://slack.com/api/chat.postMessage'
    response = requests.post(url=url, data=json.dumps(data), headers=headers)

    logging.info(response)
'''
