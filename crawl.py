import re
import sys
import requests
from bs4 import BeautifulSoup
pages = set()

def get_links(page_url):
  print(page_url)
  global pages
  global page_url2
  page_url2 = page_url
  pattern = re.compile("^(http)")
  html = requests.get(f"{page_url}").text # fstrings require Python 3.6+
  soup = BeautifulSoup(html, "html.parser")
  for link in soup.find_all("a", href=pattern):
    if "href" in link.attrs:
      if link.attrs["href"] not in pages and "krisp" not in link.attrs["href"]:
        new_page = link.attrs["href"]
        check_response(new_page)

def check_response(url):
  try:
    r = requests.get(url)
    if r.status_code != 200:
      print(10*"*")
      print(f"{r.status_code} - {url}")
      print(10*"*")
      with open('broken.txt', 'a') as broken:
        broken.write(r.status_code+"\n"+url+"-"+new_page+"\n")
  except:
    print(10*"*")
    print("No Response - "+url)
    print(10*"*")
    with open('broken.txt', 'a') as broken:
      broken.write("No Response"+"\n"+page_url2+" - "+url+"\n"+"-------"+"\n")

with open('links.txt', 'r') as f:
  with open('broken.txt', 'w') as broke:
      broke.write("")
  for i in f:  
    if i == "\n":
      break
    else:
      link = i.strip()
      try:
        get_links(link)
      except KeyboardInterrupt:
        sys.exit()
      except:
        print("error")
