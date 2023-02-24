import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import re
import time
import schedule

bot = telebot.TeleBot('6231769996:AAEPup4EY_3nUDnhtmDZke3on1wgp3OhIJo')
chat_id = '21040638'
last_job = None

def flix(url):
    client = requests.session()
    r = client.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('a[href*="gdtot"]')
    if len(links) == 0:
        links = soup.select('a[href*="filepress"]')
    links_720p = []
    links_1080p = []
    for a in links:
        link_text = a.text
        link_url = a["href"]
        size_str = re.search(r'\d+\.?\d*\s*(?:[MmGg][Bb])', link_text)
        if size_str is None:
            continue
        size_value = float(re.sub(r'[^\d.]', '', size_str.group()))
        if size_value < 2000:
            if "720p" in link_text:
                links_720p.append((link_text, link_url))
            elif "1080p" in link_text:
                links_1080p.append((link_text, link_url))
    return (links_720p, links_1080p)

def scrape_links():
    global last_job
    last_job = bot.send_message(chat_id, "Scraping links...")
    root_url = 'https://teluguflix.site/category/recently-added-movies/'
    client = requests.session()
    r = client.get(root_url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('div.item-article')
    for link in links:
        url = link.select_one('h2 a')['href']
        title = link.select_one('h2 a').text
        links_720p, links_1080p = flix(url)
        num_links = len(links_720p) + len(links_1080p)
        bot.send_message(chat_id, f"{title}\nNumber of links: {num_links}")
        time.sleep(10)
        if len(links_720p) > 0:
            bot.send_message(chat_id, "720p Links:")
            for link in links_720p:
                bot.send_message(chat_id, link[0])
                bot.send_message(chat_id, link[1])
                time.sleep(10)
        if len(links_1080p) > 0:
            bot.send_message(chat_id, "1080p Links:")
            for link in links_1080p:
                bot.send_message(chat_id, link[0])
                bot.send_message(chat_id, link[1])
                time.sleep(10)
    last_job = None

@bot.message_handler(commands=['scrapet'])
def start_scraping(message):
    global last_job
    if last_job:
        bot.send_message(chat_id, "A scraping job is already running.")
    else:
        last_job = bot.send_message(chat_id, "Starting scraping links...")
        scrape_links()

@bot.message_handler(commands=['stop'])
def stop_scraping(message):
    global last_job
    if last_job:
        bot.delete_message(chat_id, last_job.message_id)
        last_job = None
        bot.send_message(chat_id, "Scraping links has been stopped.")
    else:
        bot.send_message(chat_id, "There is no active job to stop.")

@bot.message_handler(commands=['restart'])
def restart(message):
    global last_job
    if last_job:
        bot.delete_message(chat_id, last_job.message_id)
        last_job = None
        bot.send_message(chat_id, "Scraping links has been stopped.")
    last_job = bot.send_message(chat_id, "Restarting scraping links...")
    scrape_links(message)

# Define bot commands
bot_commands = [
    types.BotCommand("/start", "Start the bot"),
    types.BotCommand("/scrapet", "Scrape links from teluguflix.site"),
    types.BotCommand("/stop", "Stop the current scraping job"),
    types.BotCommand("/restart", "Stop the current scraping job and start a new one")
]

# Set bot commands
bot.set_my_commands(bot_commands)


# Define the scraping job
def scrape_links_job():
    bot.send_message(chat_id, "Scraping links...")
    root_url = 'https://teluguflix.site/category/recently-added-movies/'
    client = requests.session()
    r = client.get(root_url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.select('div.item-article')
    for link in links:
        url = link.select_one('h2 a')['href']
        title = link.select_one('h2 a').text
        links_720p, links_1080p = flix(url)
        num_links = len(links_720p) + len(links_1080p)
        bot.send_message(chat_id, f"{title}\nNumber of links: {num_links}")
        time.sleep(10)
        if len(links_720p) > 0:
            bot.send_message(chat_id, "720p Links:")
            for link in links_720p:
                bot.send_message(chat_id, link[0])
                bot.send_message(chat_id, link[1])
                time.sleep(10)
        if len(links_1080p) > 0:
            bot.send_message(chat_id, "1080p Links:")
            for link in links_1080p:
                bot.send_message(chat_id, link[0])
                bot.send_message(chat_id, link[1])
                time.sleep(10)

# Schedule the scraping job to run every 4 hours
schedule.every(4).hours.do(scrape_links_job)

# Run the bot
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
