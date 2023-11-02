from lxml import html
import requests

def get_horoscope(sign):
    if sign == "info":
        return "Horoscope is provided by https://www.express.co.uk/horoscope"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
    }
    page = requests.get(f"https://www.express.co.uk/horoscope/{sign}/daily-forecast/today", headers=headers)
    tree = html.fromstring(page.content)
    horoscope = f"({tree.xpath('//article//h2/text()')[0]}) " + sign.capitalize()+ ":" + tree.xpath("(//article//p)[2]/text()")[0]
    return horoscope

def get_horoscope2(sign):
    if sign == "info":
        return "Horoscope is provided by https://www.freehoroscopedaily.com"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
    }
    page = requests.get(f"https://www.freehoroscopedaily.com/{sign}/", headers=headers)
    tree = html.fromstring(page.content)
    horoscope = sign.capitalize()+ ": " + tree.xpath("//div[@id='main']//p/text()")[0]
    return horoscope