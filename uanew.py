import urllib.parse
import urllib.request


params = {"q": "python programming"}

data = urllib.parse.urlencode(params)
data = data.encode("utf-8")
url = "https://www.google.com/search?" + str(data)
headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

res = urllib.request.Request(url, headers = headers)
req = urllib.request.urlopen(res)
resp =  req.read()
with open("google.html", "wb") as f:
    f.write(resp)