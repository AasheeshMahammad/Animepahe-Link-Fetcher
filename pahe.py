import requests,re
from bs4 import BeautifulSoup


def find_link(data):
    tags = BeautifulSoup(data,"lxml")
    scripts = tags.find_all("script")
    urlPat = re.compile(r'https?:[/.A-Za-z0-9]+')
    for script in scripts:
        data = urlPat.findall(str(script))
        for i in data:
            if not i.endswith('.js'):
                return i
    return None

def decode(url = ""):
    if url == "":
        return url
    try:
        req = requests.get(url)
    except Exception as e:
        return e
    data = req.text
    temp = find_link(data)
    if temp is not None:
        url = temp
    return url

def main():
    url = input("Enter :")
    print(decode(url))

if __name__ == "__main__":
    main()