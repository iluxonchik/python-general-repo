# python fenix_download login_file <url> -e <file_extension> (DEFAULT = pdf) -d <download_directory>
#
#

from fenix import Fenix
from exceptions import LoginFailedException
from bs4 import BeautifulSoup
import json, argparse, os, re
from urllib.request import urlretrieve

def parse_user(file_name):
    """
    Parse user credentials from the json file
    """    
    with open(file_name, 'r') as f:
        return json.load(f)["user"]

def get_download_path(dl_dir, file_url):
    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)

    # get the last part of url as file_name
    file_name = file_url.split("/")[-1]
    return dl_dir + '/' + file_name

# TODO: this should be a method in Fenix API
def download_file(fenix, url, file):
    with open(file, 'wb') as f:
        f.write(fenix.open(url).read())


def main(url, login_file, file_ext, dl_dir):
    user = parse_user(login_file) # get login credentials
    fenix = Fenix(user["username"], user["password"]).login()

    if fenix is None:
        raise LoginFailedException('Could not log in, please make sure that the provided credentials ' +
                                 'are correct.' )
    # TODO: exception handling
    html = fenix.open(url)
    bsObj = BeautifulSoup(html, 'html.parser')
    content_div = bsObj.find('div', {'class':'col-sm-9 main-content'})
    # maybe trust internal links only? add an opt to argparse
    anchors = content_div.findAll('a', {'href':re.compile('^(http)(.)*(.' + file_ext + ')$')})
    
    for anchor in anchors:
        dl_path = get_download_path(dl_dir, anchor['href'])
        print('Downloading ' + dl_path + " ...")
        download_file(fenix, anchor['href'], dl_path)

if __name__ == '__main__':
    # TODO: argparse
    parser = argparse.ArgumentParser(description='Download files from Fenix Edu pages')
    parser.add_argument('url', type=str, help='url from where to download the files from')
    parser.add_argument('-l', '--login', type=str, default="login.json" , help='path to fenix login credentials file (check login.json for format)')
    parser.add_argument('-e', '--extension', type=str, default='pdf', help='file extensions to download, without the leading "." (* for all, default is "pdf")')
    parser.add_argument('-d', '--directory', type=str, default='download', help='download directory')
    args = parser.parse_args()

    main(args.url, args.login, args.extension, args.directory)