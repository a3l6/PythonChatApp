import requests
from urllib.request import urlopen
import re as r

def get_mainserver() -> str:
    r = requests.get("https://raw.githubusercontent.com/Ironislife98/PythonChatApp/custom-servers/mainserverip.txt")
    #print(f"Content: {str(r.content)} of type {type(str(r.content))}")
    return str(r.content)[2:-1]

def getIP():
    d = str(urlopen('http://checkip.dyndns.com/')
            .read())
 
    return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)