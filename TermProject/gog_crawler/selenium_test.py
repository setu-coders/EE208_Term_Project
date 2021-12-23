# -*- coding: utf-8 -*-
from selenium import webdriver
import os
import math
import re
import string
import sys

#url = 'https://www.gog.com/zh/game/cyberpunk_2077'

def get_url_sel(url):
    browser = webdriver.Chrome()
    browser.get(url)
    contents = browser.page_source
    browser.close()
    return contents

if __name__ == "__main__":
    url = "https://www.gog.com/zh/game/disco_elysium"
    add_page_to_folder("disco", get_url_sel(url))
