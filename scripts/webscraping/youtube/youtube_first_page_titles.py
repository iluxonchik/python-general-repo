from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, io
# Windows console uses the cp437 encoding, which only supports 256 characters,
# wich means that some unicode chars can't be rendered, so one quick fix is 
# to escape those chars and print their actual code instead of rendering them.

# backslashreplace = replace with backslashed escape sequences (escape unsuported chars)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')

if (len(sys.argv) != 2):
	print("Usage: python youtube_first_page_titles.py <search query>")
	sys.exit(-1)


query = sys.argv[1].replace(" ", "+")

html = urlopen("https://www.youtube.com/results?search_query=" + query)
bsObj = BeautifulSoup(html, "html.parser")

titles = bsObj.findAll("a", {"class":"yt-uix-tile-link"})

for title in titles:
	print(title['title'])