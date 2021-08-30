from config import USERNAME, PASSWORD, LOGIN
import requests

r = requests.post(LOGIN, auth=(USERNAME, PASSWORD))
print(r.text)