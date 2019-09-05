import requests
from bs4 import BeautifulSoup
from .NeuroscienceNewsArticle import NeuroscienceNewsArticle

import functools
import operator

from pathlib import Path

from datetime import datetime

neuro_genres = {
    "ai" : ("https://neurosciencenews.com/neuroscience-topics/artificial-intelligence-2/", 31),
    "robotics" : ("https://neurosciencenews.com/neuroscience-topics/robotics-2/", 18),
    "psychology" : ("https://neurosciencenews.com/neuroscience-topics/psychology/", 328),
    "neurology" : ("https://neurosciencenews.com/neuroscience-topics/neurology/", 307),
    "neuroscience" : ("https://neurosciencenews.com/neuroscience-topics/neuroscience/", 579),
}

class NeuroscienceNewsSiteScraper:
    
    def __init__(self):
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

    def __get_article_urls(self, page):
        r = requests.get(page)
        raw_html = r.content
        soup_html = BeautifulSoup(raw_html, "html.parser")
        
        if 'psychology' in page:
            return [article.a['href'] for article in soup_html.findAll("div", class_="cb-article-meta")]
        
        return [article.a['href'] for article in soup_html.findAll("div", class_="cb-meta clearfix")]

    def scrape_genre_for_article_urls(self, genre_url, page_amount):
        page_num = "page/{num}/"
        url = genre_url+page_num
        pages = [url.format(num=page) for page in range(1, page_amount+1)]
        urls_from_pages = [self.__get_article_urls(page) for page in pages]
        return functools.reduce(operator.iconcat, urls_from_pages, [])

class NeuroscienceNewsArticleScraper:
    
    def __init__(self):
        self.__headers = requests.utils.default_headers()
        self.__headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

    def get_article_html(self, url):
        try:
            return requests.get(url=url, headers=self.__headers, verify=False).content
        except Exception as e:
            pass
    
    def scrape_article(self, raw_html):
        if raw_html is not None:
            
            soup_html = BeautifulSoup(raw_html, 'html.parser')

            try:
                # Commence Article Scraping
                a_title = self.__retrieve_article_title(soup_html)
                a_p = self.__retrieve_p_elements(soup_html, True)
                a_raw_p = self.__retrieve_p_elements(soup_html)
                a_tags = self.__retrieve_article_tags(soup_html)
                a_image = self.__retrieve_article_image(soup_html)
                a_date = self.__retrieve_article_upload_date(soup_html)
                a_url = self.__retrieve_article_url(soup_html)

                article = NeuroscienceNewsArticle(a_title, a_p, a_raw_p, a_tags, a_image, a_date, a_url)

                return article

            except Exception as e:
                pass
            
    def __retrieve_article_title(self, soup_html):
        return soup_html.find('title').text
    
    def __retrieve_article_url(self, soup_html):
        return soup_html.find("meta", property="og:url")['content']

    def __retrieve_p_elements(self, soup_html, get_text=False):
        if get_text:
            return [p.text for p in soup_html.findAll('p')][:-3]

        return [str(p) for p in soup_html.findAll('p')[:-3]]

    def __retrieve_article_tags(self, soup_html):
        return [tag.text for tag in soup_html.findAll("span", class_="cb-element")]
    
    def __retrieve_article_upload_date(self, soup_html):
        return soup_html.find("time", class_="entry-date updated").text

    def __retrieve_article_image(self, soup_html):
        img_dict = {}
        
        # Information to retrieve
        img_link = soup_html.find("meta", property="og:image:secure_url")['content']
        img_text = soup_html.find("p", class_="wp-caption-text").text

        img_dict['link'] = img_link
        img_dict['text'] = img_text

        return img_dict
