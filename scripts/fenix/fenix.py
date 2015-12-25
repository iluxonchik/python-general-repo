# Fenix Edu Pseudo-API
# ################################################################################################################
# This is a simple pseudo-API for Fenix Edu, created just to simplify scraping from fenix, this needs to be
# re-worked.
#
# ################################################################################################################
# Example Usage:
# 
# fenix = Fenix("ist1+++++", "<PASSWORD>")
# fenix = fenix.login() ----> NOTE: "fenix" will be None if login fails
# 
# if fenix is not None:
#   response = fenix.open(<URL>) ---> returns the response for the requested URL
#
# ################################################################################################################

import urllib.parse, urllib.request, http.cookiejar
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class Fenix(object):
    USER_AGENT_HEADER = ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
    KEEP_ALIVE_HEADER = ('Connection', "keep-alive")
    OPENER_HEADERS = [USER_AGENT_HEADER, KEEP_ALIVE_HEADER]
    LOGIN_URL = "https://id.tecnico.ulisboa.pt/cas/login"
    STUDENT_URL = "https://fenix.tecnico.ulisboa.pt/student/"

    def __init__(self, username, password):
        self.username = username # this shouldn't be stored as plain text, only like this for demo purposes
        self.password = password
        self.opener = None

    def login(self):
        """
        Logins the user with the credentials specified on object instantiation.

        Returns:
            Fenix object (self) on login success
            None on login failure
        """
        cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        self.opener.addheaders = Fenix.OPENER_HEADERS
        
        # Let's parse the needed "lt" and "execution" values (needed for POST request, when logging in)
        try:
            res = self.opener.open(Fenix.LOGIN_URL)
        except HTTPError:
            return None

        bsObj = BeautifulSoup(res, "html.parser")
        lt = bsObj.find('input', {'type':'hidden', 'name':'lt'}).attrs['value']
        execution = bsObj.find('input', {'type':'hidden', 'name':'execution'}).attrs['value']

        # Build the POST request
        values = {"username" : self.username, "password" : self.password, "submit-istid" : "Entrar", "lt" : lt, "execution" : execution, "_eventId":"submit"}
        data = urllib.parse.urlencode(values)
        binary_data = data.encode("ascii")

        try:
            res = self.opener.open(Fenix.LOGIN_URL, binary_data) # send the post request, after that we should be logged in
            # Get the sessionid cookie
            res = self.opener.open("https://id.tecnico.ulisboa.pt/cas/login?service=https%3A%2F%2Fbarra.tecnico.ulisboa.pt%2Flogin%2F%3Fnext%3Dhttps%253A%252F%252Fid.tecnico.ulisboa.pt%252Fcas%252Flogin%253Fservice%253Dhttps%253A%252F%252Ffenix.tecnico.ulisboa.pt%252FloginCAS.do")
            # Get the csrftoken cookie | NOTE: this one isn't required
            res = self.opener.open("https://barra.tecnico.ulisboa.pt/include/?fluid=true&login=https://fenix.tecnico.ulisboa.pt/login&lang=pt&logout=https://fenix.tecnico.ulisboa.pt/logout&next-param=service")
        except HTTPError:
            return None

        return self if self.is_logged_in() else None
        
    def open(self, url, data=None):
        return self.opener.open(url, data)

    def is_logged_in(self):
        """
        Checks whether the current instance is associated with a logged in user.
        """
        # Try to access a protected resource (only logged in users can access it),
        # in case the instance is not associated with a logged in user, HTTPError with
        # error code 404 is raised. In this case, if some other HTTPError occurs, this
        # will return false as well

        # TODO: 
        #   * more efficient way of checking if user is logged in
        #   * create and raise exceptions for not logged in case     
        #
        if self.opener is not None:
            try:
                self.opener.open(Fenix.STUDENT_URL)
                return True
            except HTTPError: 
                return False
        return False
