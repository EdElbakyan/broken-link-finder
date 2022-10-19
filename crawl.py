import re
import requests
from bs4 import BeautifulSoup

pages = set()

def get_links(page_url):
  print(page_url)
  with open('sites.txt', 'a') as file:
    file.write("--------------------\n"+page_url+"\n--------------------\n")
  global pages
  pattern = re.compile("^(http)")
  html = requests.get(f"{page_url}").text # fstrings require Python 3.6+
  soup = BeautifulSoup(html, "html.parser")
  for link in soup.find_all("a", href=pattern):
    if "href" in link.attrs:
      if link.attrs["href"] not in pages and "krisp" not in link.attrs["href"]:
        new_page = link.attrs["href"]
        check_response(new_page)
        with open('sites.txt', 'a') as file:
          file.write(new_page+"\n")

def check_response(url):
  try:
    r = requests.get(url)
    if r.status_code != 200:
      print(10*"*")
      print("\n")
      print("\n")
      print("\n")
      print(f"{r.status_code} - {url}")
      print("\n")
      print("\n")
      print("\n")
      print(10*"*")
  except requests.exceptions.ConnectionError as e:
    print("No Response - "+url)

with open('links.txt', 'r') as f:
  for i in f:  
    if i == "\n":
      break
    else:
      link = i.strip()
      get_links(link)
