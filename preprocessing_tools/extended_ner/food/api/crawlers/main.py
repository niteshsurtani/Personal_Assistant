from bs4 import BeautifulSoup
import socket
import requests
from re import sub
from city import cityList
from locality import find_locality


locality = find_locality('Pune')