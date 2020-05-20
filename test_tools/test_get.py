import requests
import webbrowser
import os

IP = '127.0.0.1'
PORT = '8000'
SIZE = 'leaderboard'
KEY = 'P53ZD2pSaQdg43oWK1Fuop2VIysPO9p0'
KEY = 'fqXKaCiNoSksZE8ZqoZpvsMiPLMfwWWM'
FILENAME = 'ad_get.html'
"""
url link: https://<domain-name>/api/<size>/<key>
"""

r = requests.get(f"http://{IP}:{PORT}/api/{SIZE}/{KEY}")
r = r.json()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME)
with open(path, "w") as f:
    f.write(r)
webbrowser.open(path, new=2)