# python fenix_download login_file <url> -e <file_extension> (DEFAULT = pdf) -d <download_directory>
#
#

from fenix import Fenix
import argparse

if __name__ == '__main__':
    # TODO: argparse
    parser = argparse.ArgumentParser(description='Download files from Fenix Edu pages')
    parser.add_argument('login', type=str, help='path to fenix login credentials file (check login.json for format)')
    parser.add_argument('url', type=str, help='url from where to download the files from')
    parser.add('-e', '--extension', type=str, default='pdf', help='file extensions to download, without the leading "." (* for all, default is "pdf")')
    parser.add('-d', '--directory', type=str, default='download', help='download directory')