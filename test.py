import tkinter as ttk
from tkinter import filedialog
from tkinter import messagebox
import httplib2
import json
import urllib
import pandas as pd

url = "https://www.interrep.com.br/api/"
http = httplib2.Http()
content = http.request(url + 'seriea' + '/players/active',
                       method='GET',
                       headers={'Content-Type': 'application/x-www-form-urlencoded',
                                'Authorization': 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjogMSwgImV4cCI6IDE3MDQwMzcyNDB9.R8ZU26PXkOrTaD1WWghep-eFV8eSzi7I6kVyhuEs3kk'})[1]
response = json.loads(content.decode('utf-8'))
allPlayerList = response