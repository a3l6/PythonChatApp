import requests

def get_mainserver() -> str:
    r = requests.get("https://raw.githubusercontent.com/Ironislife98/PythonChatApp/main/log-2022-11-09.txt")
    return r.content