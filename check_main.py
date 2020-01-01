from selenium import webdriver  # installしたseleniumからwebdriverを呼び出せるようにする
from selenium.webdriver.common.keys import Keys  # webdriverからスクレイピングで使用するキーを使えるようにする。
import slackweb
import datetime

python_URL = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=python&useSynonym=1&vendor=&product=&datePublicFromYear=&datePublicFromMonth=&datePublicToYear=&datePublicToMonth=&dateLastPublishedFromYear=&dateLastPublishedFromMonth=&dateLastPublishedToYear=&dateLastPublishedToMonth=&v3Severity%5B%5D=01&cwe=&searchProductId="
django_URL = "https://jvndb.jvn.jp/search/index.php?mode=_vulnerability_search_IA_VulnSearch&lang=ja&keyword=django&useSynonym=1&vendor=&product=&datePublicFromYear=&datePublicFromMonth=&datePublicToYear=&datePublicToMonth=&dateLastPublishedFromYear=&dateLastPublishedFromMonth=&dateLastPublishedToYear=&dateLastPublishedToMonth=&v3Severity%5B%5D=01&cwe=&searchProductId="

webdriver = webdriver.Chrome()
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
slack = slackweb.Slack(url="")

str_time = "===" + str(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')) + "の最新のPython脆弱性(緊急度9以上)==="
slack.notify(text=str_time)
slack.notify(text=get_jvn_info(webdriver))

webdriver.get(django_URL)

str_time = "===" + str(dt_now.strftime('%Y年%m月%d日 %H:%M:%S')) + "の最新のDjango脆弱性(緊急度9以上)==="
slack.notify(text=str_time)
slack.notify(text=get_jvn_info(webdriver))

slack.notify(text="============")
print("Slackへの投稿完了")
