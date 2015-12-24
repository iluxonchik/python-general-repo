# Fenix Edu Login
# ################################################################################################################
# This script is a demo of logging in to fenixedu platform.
#
# You might be wondering what's up with all of the hardcoded url requests after sending the login
# credentials? Well, by analysing the requests you can see that when loading pages, your browser sends
# some cookies to the webserver, which were set up by the webserver in the first place. Some of those
# cookies are required, so that the webservers knows who's logged in and the login is in fact valid.
# When using a webbrowser, he makes requstes to load resources "automatically" (for example, he might run
# a script which requests to load a page, so the web browser goes ahead and requests that resource for him),
# our script however, does not do that, it does exactly what we tell him to do: loads only what we asked him.
# That means that we have to send him to load those pages, so that they can set the cookies (via "Set-Cookie"
# header), which will then be used in future requests we make.
#
# This code isn't exactly well modularized, it's just a quick demo.
# ################################################################################################################

import urllib.parse, urllib.request, http.cookiejar
from bs4 import BeautifulSoup

# Fenix Edu Login Credentials #
################################
USERNAME = "ist1+++++"
PASSWORD = "+PASSWORD+"
################################

USER_AGENT_HEADER = ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
KEEP_ALIVE_HEADER = ('Connection', "keep-alive")
OPENER_HEADERS = [USER_AGENT_HEADER, KEEP_ALIVE_HEADER]
LOGIN_URL = "https://id.tecnico.ulisboa.pt/cas/login"

cj = http.cookiejar.CookieJar()

op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = OPENER_HEADERS

# Let's parse the needed "lt" and "execution" values (needed for POST request, when logsging in)
res = op.open(LOGIN_URL)
bsObj = BeautifulSoup(res, "html.parser")
lt = bsObj.find('input', {'type':'hidden', 'name':'lt'}).attrs['value']
execution = bsObj.find('input', {'type':'hidden', 'name':'execution'}).attrs['value']

# Build the POST request
values = {"username":USERNAME, "password":PASSWORD, "submit-istid" : "Entrar", "lt" : lt, "execution" : execution, "_eventId":"submit"}
data = urllib.parse.urlencode(values)
binary_data = data.encode("ascii")
res = op.open(LOGIN_URL, binary_data) # send the post request, after that we should be logged in

# Get the sessionid cookie
res = op.open("https://id.tecnico.ulisboa.pt/cas/login?service=https%3A%2F%2Fbarra.tecnico.ulisboa.pt%2Flogin%2F%3Fnext%3Dhttps%253A%252F%252Fid.tecnico.ulisboa.pt%252Fcas%252Flogin%253Fservice%253Dhttps%253A%252F%252Ffenix.tecnico.ulisboa.pt%252FloginCAS.do")

# Get the csrftoken cookie | NOTE: this one isn't required
res = op.open("https://barra.tecnico.ulisboa.pt/include/?fluid=true&login=https://fenix.tecnico.ulisboa.pt/login&lang=pt&logout=https://fenix.tecnico.ulisboa.pt/logout&next-param=service")

# Now we can make requests to any pages protected by login, happy scraping!
res = op.open("https://fenix.tecnico.ulisboa.pt/student/") # load demo page
print(BeautifulSoup(res, "html.parser"))