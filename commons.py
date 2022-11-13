import requests

def get_mainserver() -> str:
    r = requests.get("https://raw.githubusercontent.com/Ironislife98/PythonChatApp/custom-servers/mainserverip.txt")
    print(f"Content: {str(r.content)} of type {type(str(r.content))}")
    return str(r.content)