from slacker import Slacker


def slack_mapianist(url, comment):
    token = ''
    channel = ''
    username = ''
    icon_url = ''
    if url != 'none':
        attachments = [{
            'title': '확인하기',
            'title_link': url,
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
