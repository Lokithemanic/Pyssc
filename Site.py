"""website-update-check in Python
This program makes it possible to track changes of a website.
It downloads the website you enter every x seconds and compares its md5
hashes to detect changes. You can even use Pushovers API to send
custom notifications to your Android phone or iPhone.
"""

from datetime import datetime
import hashlib
import os
import time

from bs4 import BeautifulSoup
from pushover import init, Client  # push notifications to your phone
import requests
#import vlc  # needed for the music feature
# set the path to the music if you want to use this feature


class Md5:
    """This class holds md5 values.
    """

    original_md5sum = ""
    new_md5sum = ""


class Settings:
    """This class saves the user's settings.
    """

    url = "https://ssc.nic.in"
    push = True
    update_timer = 60


def check_for_update():
    """This function downloads the website and calculates hashes
    This function downloads the website using the requests module,
    then it strips HTML tags off so that raw text is left.
    Then it calculates md5 hashes of this text to detect any
    changes over time.
    """

    if os.path.isfile("website.txt"):
        request = requests.get(Settings.url)
        assert request.status_code == 200
      #  print("connected successfully")
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        with open("website_new.txt", "w") as f:
            f.write(text)
        hasher = hashlib.md5()
        with open('website_new.txt', 'rb') as f:
            buffer = f.read()
            hasher.update(buffer)
        Md5.new_md5sum = hasher.hexdigest()

    else:
        request = requests.get(Settings.url)
        assert request.status_code == 200
        html = request.text
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        with open("website.txt", "w") as f:
            f.write(text)
        hasher = hashlib.md5()
        with open('website.txt', 'rb') as f:
            buffer = f.read()
            hasher.update(buffer)
        Md5.original_md5sum = hasher.hexdigest()
        check_for_update()


def main():
    """This function takes the user's wished settings as input
    This function not only takes input from the user but also
    cautiously handles it and checks its validity.
    """

    path = os.path.dirname(os.path.realpath(__file__))
    try:
        os.remove(path + "/website.txt")
    except OSError:
        pass
    try:
        os.remove(path + "/website_new.txt")
    except OSError:
        pass

    check_for_update()
    mainloop()


def mainloop():
    """This function is the clock generator of this program
    This function creates the loop which checks if any
    changes on a given website occur over time.
    """

    while True:
        check_for_update()
        '''
        print("Original: ", original_md5sum)
        print("New: ", new_md5sum)
        '''
        if Md5.original_md5sum == Md5.new_md5sum:
            print("Nothing there! " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("Result is out. Maybe :/" +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            if Settings.push:
                init("anub5bu2j19hk7iovfrk7c4pjdxsrk")
                Client("ut7x3c9hizi7res7gisx5oh7oyyiub").send_message("Result is out!! maybe :/", title="CHSL 17")
        time.sleep(Settings.update_timer)

if __name__ == "__main__":
    main()