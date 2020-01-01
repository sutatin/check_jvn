from selenium import webdriver  # installしたseleniumからwebdriverを呼び出せるようにする
from selenium.webdriver.common.keys import Keys  # webdriverからスクレイピングで使用するキーを使えるようにする。
import slackweb
import datetime
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1280,1024')

python_URL = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=python&useSynonym=1&vendor=&product=&datePublicFromYear=&datePublicFromMonth=&datePublicToYear=&datePublicToMonth=&dateLastPublishedFromYear=&dateLastPublishedFromMonth=&dateLastPublishedToYear=&dateLastPublishedToMonth=&v3Severity%5B%5D=01&cwe=&searchProductId="
django_URL = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=django&useSynonym=1&vendor=&product=&datePublicFromYear=&datePublicFromMonth=&datePublicToYear=&datePublicToMonth=&dateLastPublishedFromYear=&dateLastPublishedFromMonth=&dateLastPublishedToYear=&dateLastPublishedToMonth=&v3Severity%5B%5D=01&cwe=&searchProductId="
slack_hook_URL = ""

webdriver = webdriver.Chrome(chrome_options=options)
webdriver.get(python_URL)


def get_jvn_info(web_driver):
    titles = web_driver.find_elements_by_css_selector("tr")
    counter = 0
    for title in titles:
        if counter == 12:
            print(title.text)
            str_slack = str(title.text)
            break
        counter += 1
    return str_slack


dt_now = datetime.datetime.now()
slack = slackweb.Slack(url=slack_hook_URL)

str_time = "===" + str(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')) + "の最新のPython脆弱性(緊急度9以上)==="
slack.notify(text=str_time)
slack.notify(text=get_jvn_info(webdriver))

webdriver.get(django_URL)

str_time = "===" + str(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')) + "の最新のDjango脆弱性(緊急度9以上)==="
slack.notify(text=str_time)
slack.notify(text=get_jvn_info(webdriver))

slack.notify(text="============")

webdriver.quit()

print("Slackへの投稿完了")
