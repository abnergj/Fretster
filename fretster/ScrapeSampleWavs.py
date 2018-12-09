"""
Module that downloads .wav files from
https://freewavesamples.com
"""
from bs4 import BeautifulSoup as bsoup
import requests
import os

"""
Class to handle downloading the sample files
"""


class WavDownloader:
    # Urls
    _SITE_URL = "https://freewavesamples.com"
    _DOWNLOAD_URL = "https://freewavesamples.com/files"

    # Returns a tuple containing the BeautifulSoup object of
    # the passed url and the request status code.
    @staticmethod
    def soupRequest(url):
        page = requests.get(url)
        return bsoup(page.text, 'html.parser'), page.status_code

    # Checks if the url is downloadable. Taken from:
    # https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
    @staticmethod
    def is_downloadable(url):
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            print("content-type: text")
            return False
        if 'html' in content_type.lower():
            print("content-type: html")
            return False
        return True

    # Downloads the .wav file at the given url. This is not
    # a particularly safe method so on the off chance someone
    # else is reading this, be very careful. If folderPath is not
    # defined, the file will be saved in the cwd. The file name
    # matches the filename on the site. If overwrite is set to
    # true, then any file with a matching name will be deleted 
    # and the downloaded file will replace it.
    @staticmethod
    def downloadWav(wavUrl, folderPath=None, overwrite=False):
        # Adds folder path and removes the beginning of the url
        fname = folderPath + wavUrl[34:]

        # Input Validation
        if not WavDownloader.is_downloadable(wavUrl):
            print(f"File at address '{wavUrl}' is not downloadable")
            return

        if fname[-3:] != 'wav':
            print('Incorrect file type')
            return

        if folderPath and not os.path.exists(folderPath):
            print(f"Folder '{folderPath}' does not exist'")
            return

        if os.path.exists(fname):
            # Deletes if overwrite is true
            if overwrite:
                print(f"File '{fname}' already exists. Deleting.")
                os.remove(fname)
            else:
                print(f"File '{fname}' already exists")
                return

        # Attempts to download the wav file. Catches
        # and prints the message of any exception
        try:
            r = requests.get(wavUrl, allow_redirects=True)
            with open(folderPath + wavUrl[34:], 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print("Error Downloading File: ")
            print(e)
            try:
                print(f"Status Code: {r.status_code}")
            except Exception:
                pass

    """
    The WavDownloader class only contains a dict that keeps track of the
    categories of samples. The dictionary has form:

    {'category' : [List of subcategories]}
    """

    def __init__(self):
        self.categories = {}
        self.scrapeCategories()

    # Creates the categories dict
    def scrapeCategories(self):
        pSoup, _ = WavDownloader.soupRequest(WavDownloader._SITE_URL)
        categoryLinks = [pTag.a['href'] for pTag in
                         pSoup.find_all(class_='leafnode') + pSoup.find_all(class_="parentnode")]

        categoryLinks = list(map(lambda href: href.split('/')[2:], categoryLinks))
        self.categories = {k[0]: [] for k in categoryLinks if len(k) == 1}
        for link in categoryLinks:
            if len(link) == 2:
                self.categories[link[0]].append(link[1])

                # Returns the keys of the categories dictionary

    def getCategories(self):
        return self.categories.keys()

    # Gets the list of subcategories of a given category. Generates 
    def getSubCategory(self, category):
        if category not in self.getCategories():
            raise ValueError
        return self.categories[category]

    # Creates the url for the first page of samples for a given
    # category/subcategory.
    def createBaseUrl(self, category=None, subCategory=None):
        url = self._SITE_URL
        if category in self.categories.keys():
            url += '/sample-type/' + category
            if subCategory in self.categories[category]:
                url += '/' + subCategory
        return url

    # Returns a list of links to the .wav samples. If a subCategory
    # is passed then a valid category must also be passed.
    def getDownloadLinks(self, category=None, subCategory=None):

        # A generator for returning the links. 
        def downloadGen(base):

            lastSoup, lastCode = WavDownloader.soupRequest(base)
            i = 0
            while lastCode != 404:
                for samp in lastSoup.find_all(class_='sample'):
                    href = samp.h2.a['href']
                    hrefSoup, _ = self.soupRequest(self._SITE_URL + '/' + href)
                    downloadURL = self._SITE_URL + '/' + hrefSoup.find(class_='graylink').a['href']
                    catlist = hrefSoup.find(class_="catname").find_all('a')
                    cat = catlist[0]['href'].split('/')[-1]
                    subCat = catlist[1]['href'].split('/')[-1] if len(catlist) > 1 else None
                    yield (downloadURL, cat, subCat)

                i += 1
                lastSoup, lastCode = WavDownloader.soupRequest(base + f"/?page={i}")

        # Input Validation
        if category and category not in self.categories.keys():
            raise ValueError
        if subCategory:
            if not category or subCategory not in self.categories[category]:
                raise ValueError

        # Fetches List
        baseUrl = self.createBaseUrl(category=category, subCategory=subCategory)
        return [x for x in downloadGen(baseUrl)]

    # TODO: Fix this shit so everything is saved to the right directory. Commented code is a start
    def download(self,folderpath="D:\\DataDumps\\FreeWaveSamplesDump", category=None, subCategory=None):

        downloadList = self.getDownloadLinks(category=category, subCategory=subCategory)
        for info in downloadList:
            url, cat,subcat = info
            path = folderpath + "\\" + cat.title()
            if not os.path.isdir(path): os.mkdir(path)
            if subcat:
                path += "\\" + subcat.title()
                if not os.path.isdir(path):
                    os.mkdir(path)
            try:
                self.downloadWav(info[0],path)
            except Exception as e:
                print(f"Exception downloading file @ '{url}'")
                print(e)


if __name__ == "__main__":
    categories = ['guitar', 'bass', 'synthesizer', 'drums']

    wd = WavDownloader()
    for cat in categories:
        try:
            wd.download(category=cat)
            print(f"Passed {cat}")
        except Exception as e:
            print(f"Failed at {cat}")
            print(e)