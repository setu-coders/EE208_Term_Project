import os
import math
import re
import string
import sys
from typing import final
import urllib
import requests
import urllib.error
import urllib.parse
import urllib.request
from urllib.request import Request, urlopen
import hashlib
import threading
import queue
import time
from bs4 import BeautifulSoup
import argparse

seeds = [f"https://www.gog.com/games?sort=title&page={i}" for i in range(1, 5)]

if __name__ == "__main__":
    