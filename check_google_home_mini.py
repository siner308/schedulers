import datetime
from logger import get_my_logger
from slack import slack_google_home_mini
from chromedriver import ChromeDriver

logger = get_my_logger('google_home_mini')


def crawling():
    chrome = ChromeDriver()
    chrome.driver.get('https://home.google.com/promotions?utm_campaign=GS104586&utm_source=support&utm_term=support&utm_content=MY')
    if not chrome.driver.title == 'Google Nest':
        logger.info(chrome.driver.page_source)
        return '[%s] 타이틀이 Google Nest가 아닌 페이지가 탐지됐어!!!' % datetime.datetime.now()

    if chrome.driver.page_source.find('Google Korea LLC에서 제공하는 프로모션 코드(쿠폰)에는 다음 약관이 적용됩니다. 쿠폰을 2020년 3월 31일 오후 11:59(KST)까지 사용하지 않으면 만료됩니다. 2020년 2월 19일 기준으로 YouTube Premium을 이용 중인 유료 회원에 한해 제공됩니다. 사용자는 쿠폰 사용 날짜를 기준으로 멤버십이 일시중지되거나, 이용을 취소 내지 비활성화한 상태가 아닌 회원이어야 합니다. 프로모션 코드당 Google Home Mini 1대를 신청할 수 있으며 재고가 소진될 때까지 선착순으로 제공됩니다.  Google은 필요에 따라 관련 약관을 수정할 권리를 유보합니다.') == -1:
        logger.info(chrome.driver.page_source)
        return '[%s] 만료 내용이 나오던 곳의 내용이 바뀌었어!!!' % datetime.datetime.now()

    if chrome.driver.page_source.find('만료된 혜택입니다.') == -1:
        logger.info(chrome.driver.page_source)
        return '[%s] 물량 들어왔나?!?!?!?!' % datetime.datetime.now()
    return '[%s] 아직 아닌가봐...' % datetime.datetime.now()


if __name__ == '__main__':
    now = datetime.datetime.now()
    logger.info('%s' % now)
    try:
        result = crawling()
        slack_google_home_mini(result)
    except Exception as e:
        slack_google_home_mini(str(e))
