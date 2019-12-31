import requests
import json
from bs4 import BeautifulSoup
from DbHandler import DbHandler


API = "xxxx"
TELEGRAM = "https://api.telegram.org/bot{}/".format(API)
MANGA_SITE = "https://demonslayermanga.com/"
db = DbHandler("DemonSlayerDB.db")


# Need to work on my get update function
def get_update(manga_url):
    source = requests.get(manga_url).text
    soup = BeautifulSoup(source, "html.parser")
    tbody = soup.find('tbody', {"class": "no-border-x"})
    tr = tbody.find('tr')
    chapter, date = tr.findAll('td')[0].text, tr.findAll('td')[1].text
    return chapter


def get_last_notified():
    return db.retrieve_data()[0]


def set_last_notified():
    chapter = get_update(MANGA_SITE)
    return chapter


def update_db(old_chapter, new_chapter):
    return db.update_values(old_chapter, new_chapter)


# Get information about the last user that sent a message
def get_information_from_last_message(telegram_url):
    update = telegram_url + "getUpdates"
    response = requests.get(update)
    content = response.content.decode("utf8")
    updates = json.loads(content)
    num_update = len(updates['result'])
    last_update = num_update - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    #usernmae = updates["result"][last_update]["message"]["chat"]["username"]
    return text, chat_id


def is_new_chapter_out(latest, saved):
    return latest != saved


def send_message(chapter, chat_id):
    if chapter[:3] is "Hey":
        message = chapter
    else:
        message = chapter + " IS OUT!!"
    send_url = "https://api.telegram.org/bot{a}/sendMessage?chat_id={c}&text={m}".format(a=API, c=chat_id, m=message)
    return requests.get(send_url)


def welcome(chat_id):
    message = "Hey, I'm bot(Didn't name him yet) who keeps you up to date with your favorite manga\n" \
           "you can use /update to see the latest chapter\n" \
           "that's all I'm still under construction you degenerate weeb"
    send_message(message, chat_id)


def main():
    text, chat_id = get_information_from_last_message(TELEGRAM)
    latest_release = get_update(MANGA_SITE)
    saved = get_last_notified()

    if text == "/start":
        welcome(chat_id)
        send_message(latest_release, chat_id)
        db.insert_values(latest_release)

    if text == "/update":
        send_message(latest_release, chat_id)

    if is_new_chapter_out(latest_release, saved):
        send_message(latest_release, chat_id)
        update_db(saved, latest_release)


if __name__ == '__main__':
    main()
