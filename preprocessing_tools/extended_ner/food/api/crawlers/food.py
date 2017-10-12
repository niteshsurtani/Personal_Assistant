from bs4 import BeautifulSoup
import socket
import requests
from re import sub
searchurl = "https://www.foodpanda.in/restaurant/m2pt/roll-mafia-viman-nagar#info"
f = requests.get(searchurl)
html = f.text
soup = BeautifulSoup(html)
string = ''
