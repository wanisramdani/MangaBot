import requests
from bs4 import BeautifulSoup
"""
But if you ask me, using the database is better:
- You can monitor multiple releases/manga
- You will gain more experience and familiarity with SQL
- You can be like: *Tut*, I used Heroku and PostgreSQL and Telegram API and BeautifulSoup, how cool is that?
"""


def get_update(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "html.parser")
    tbody = soup.find('tbody', {"class": "no-border-x"})
    tr = tbody.find('tr')
    return tr.findAll('td')


def get_last_update_chapter(url):
    chapter = get_update(url)
    return chapter[0].text

def get_last_update_date(url):
    date = get_update(url)
    return date[1].text


def get_last_notified():
    # From database or chat history
    pass


def set_last_notified():
    pass


def new_chapter_out(latest, saved):
    return latest != saved


def notify_me():
    pass


def main():
    URL = "https://demonslayermanga.com/"
    date = get_last_update_date(URL)



main()