# Scrape YouTube video title, description and keywords
# TODO: organize the code in classes
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys, io, argparse

def get_video_title(bsObj):
    """
    Returns the video title
    """
    # TODO

def get_video_description(bsObj):
    """
    Returns the video description
    """
    # TODO
    # <meta name="description" 

def get_video_tags(bsObj):
    """
    Returns a list of video tags
    """
    # TODO
    # <meta property="og:video:tag" >
    tags = bsObj.findAll("meta", {"property":"og:video:tag"})
    #print(tags)
    return get_text_on_list(tags, 'content')


def get_video_links(url):
    """
    Returns a list of videos from a page
    """
    # TODO

def get_text_on_list(elems, attr):
    """
    Recieves a collection of BS objects, retrieves "attr" attribute from each one of them 
    and returns the resulting list
    """
    return [elem.attrs[attr] for elem in elems if elem.attrs[attr] is not None]

def positive_check(value:str):
    """
    Check if the provided string is a positive integer
    """
    val = int(value)
    if val > 0:
        return val
    raise argparse.ArgumentTypeError('{} is not a postivie interger'.format(value))

if __name__  == '__main__':
    # TODO
    parser = argparse.ArgumentParser(description='Scrapes YouTube video info')
    parser.add_argument('search', help='search url or search query', type=str)
    parser.add_argument('-d', '--domain', help='search domain ("com", "co.uk", "ru", "com.br", etc) default is "com"', type=str, default="com")
    parser.add_argument('-o', '--out', help='output file name', dest='filename', type=str)
    parser.add_argument('-p', '--pages', help='number of pages to parse (starting from page 1)', type=positive_check, default=1)
    args = parser.parse_args()

    html = urlopen(args.search)
    bsObj = BeautifulSoup(html, "html.parser")
