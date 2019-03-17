from slacker import Slacker
from environments import Env

def slack_mapianist(url, comment, title=None):
    envs = Env('envs.txt')
    token = envs.data['SLACK_TOKEN']
    channel = envs.data['SLACK_CHANNEL']
    username = envs.data['SLACK_USERNAME']
    icon_url = envs.data['SLACK_ICON_URL']
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

    slack = Slacker(token)
    slack.chat.post_message(text=None, channel=channel, username=username, attachments=attachments, icon_url=icon_url)
