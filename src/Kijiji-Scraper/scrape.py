

class KijijiAd():

    def __init__(self, ad):
        self.title = ad.find('a', {"class": "title"}).text.strip()
        self.id = ad['data-listing-id']
        self.ad = ad
        self.info = {}

        self.__locate_info()
        self.__parse_info()

    def __locate_info(self):
        # Locate ad information
        self.info["Title"] = self.ad.find('a', {"class": "title"})
        self.info["Image"] = str(self.ad.find('img'))
        self.info["Url"] = self.ad.get("data-vip-url")
        self.info["Details"] = self.ad.find(
            'div', {"class": "details"})
        self.info["Description"] = self.ad.find(
            'div', {"class": "description"})
        self.info["Date"] = self.ad.find(
            'span', {"class": "date-posted"})
        self.info["Location"] = self.ad.find('div', {"class": "location"})
        self.info["Price"] = self.ad.find('div', {"class": "price"})

    def __parse_info(self):
        # Parse Details and Date information
        self.info["Details"] = self.info["Details"].text.strip() \
            if self.info["Details"] is not None else ""
        self.info["Date"] = self.info["Date"].text.strip() \
            if self.info["Date"] is not None else ""

        # Parse remaining ad information
        for key, value in self.info.items():
            if value:
                if key == "Url":
                    self.info[key] = 'http://www.kijiji.ca' + value

                elif key == "Description":
                    self.info[key] = value.text.strip() \
                        .replace(self.info["Details"], '')

                elif key == "Location":
                    self.info[key] = value.text.strip() \
                        .replace(self.info["Date"], '')

                elif key not in ["Image", "Details", "Date"]:
                    self.info[key] = value.text.strip()




#%%


import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path


class KijijiScraper():

    def __init__(self, filename="ads.json"):
        self.filepath = Path().absolute().joinpath(filename)
        self.all_ads = {}
        self.new_ads = {}

        self.third_party_ads = []
        self.exclude_list = []

        self.load_ads()

    # Reads given file and creates a dict of ads in file
    def load_ads(self):
        # If the file doesn't exist create it
        if not self.filepath.exists():
            ads_file = self.filepath.open(mode='w')
            ads_file.write("{}")
            ads_file.close()
            return
 
        with self.filepath.open(mode="r", encoding='utf8') as ads_file:
            self.all_ads = json.load(ads_file)

    # Save ads to file
    def save_ads(self):
        with self.filepath.open(mode="w") as ads_file:
            json.dump(self.all_ads, ads_file)

    # Set exclude list
    def set_exclude_list(self, exclude_words):
        self.exclude_list = self.words_to_lower(exclude_words)

    # Pulls page data from a given kijiji url and finds all ads on each page
    def scrape_kijiji_for_ads(self, url):
        self.new_ads = {}

        email_title = None
        while url:
            # Get the html data from the URL
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            # If the email title doesnt exist pull it from the html data
            if email_title is None:
                email_title = self.get_email_title(soup)

            # Find ads on the page
            self.find_ads(soup)

            # Set url for next page of ads
            url = soup.find('a', {'title': 'Next'})
            if url:
                url = 'https://www.kijiji.ca' + url['href']

        return self.new_ads, email_title

    def find_ads(self, soup):
        # Finds all ad trees in page html.
        kijiji_ads = soup.find_all("div", {"class": "search-item regular-ad"})

        # Find all third-party ads to skip them
        third_party_ads = soup.find_all("div", {"class": "third-party"})
        for ad in third_party_ads:
            thid_party_ad_id = KijijiAd(ad).id
            self.third_party_ads.append(thid_party_ad_id)

        # Create a dictionary of all ads with ad id being the key
        for ad in kijiji_ads:
            kijiji_ad = KijijiAd(ad)

            # If any of the title words match the exclude list then skip
            if not [False for match in self.exclude_list
                    if match in kijiji_ad.title.lower()]:

                # Skip third-party ads and ads already found
                if (kijiji_ad.id not in self.all_ads and
                        kijiji_ad.id not in self.third_party_ads):

                    self.new_ads[kijiji_ad.id] = kijiji_ad.info
                    self.all_ads[kijiji_ad.id] = kijiji_ad.info

    def get_email_title(self, soup):
        email_title_location = soup.find('div', {'class': 'message'})

        if email_title_location:

            if email_title_location.find('strong'):
                email_title = email_title_location.find('strong')\
                    .text.strip('"').strip(" »").strip("« ")
                return self.format_title(email_title)

        content = soup.find_all('div', class_='content')
        for i in content:

            if i.find('strong'):
                email_title = i.find('strong')\
                    .text.strip(' »').strip('« ').strip('"')
                return self.format_title(email_title)

        return ""

    # Makes the first letter of every word upper-case
    def format_title(self, title):
        new_title = []

        title = title.split()
        for word in title:
            new_word = ''
            new_word += word[0].upper()

            if len(word) > 1:
                new_word += word[1:]

            new_title.append(new_word)

        return ' '.join(new_title)

    # Returns a given list of words to lower-case words
    def words_to_lower(self, words):
        return [word.lower() for word in words]



#%%

#!/usr/bin/env python3
import yaml
import sys

if __name__ == "__main__":
    args = sys.argv
    skip_flag = "-s" in args

    # Get config values
    with open("config.yaml", "r") as config_file:
        email_config, urls_to_scrape = yaml.safe_load_all(config_file)

    # Initialize the KijijiScraper and email client
    kijiji_scraper = KijijiScraper()

    # Scrape each url given in config file
    for url_dict in urls_to_scrape:
        url = url_dict.get("url")
        exclude_words = url_dict.get("exclude", [])

        print(f"Scraping: {url}")
        if len(exclude_words):
            print("Excluding: " + ", ".join(exclude_words))

        kijiji_scraper.set_exclude_list(exclude_words)
        ads, email_title = kijiji_scraper.scrape_kijiji_for_ads(url)

        info_string = f"Found {len(ads)} new ads\n" \
            if len(ads) != 1 else "Found 1 new ad\n"
        print(info_string)

    kijiji_scraper.save_ads()
