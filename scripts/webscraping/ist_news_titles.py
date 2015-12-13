from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,'cp437','backslashreplace')

html = urlopen("http://tecnico.ulisboa.pt/pt/noticias/")
bsObj = BeautifulSoup(html, "html.parser")


for news_wrapper in bsObj.find("div", {"id":"content_wrapper"}).findAll("div", {"class":"news_wrapper"}):
	news_grid = news_wrapper.find("div", {"class":"grid_9 omega"})
	print("Date: " + news_grid.p.get_text())
	print("Title: " + news_grid.h3.a.get_text())