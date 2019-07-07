import requests
from bs4 import BeautifulSoup

class ArticleScrape:
    
    def __init__(self):
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })

    def scrape_article(self, url):
        r = requests.get(url, self.headers)
        raw_html = r.content
        soup_html = BeautifulSoup(raw_html, 'html.parser')
        
        # Commence Article Scraping
        a_title = self.__retrieve_article_title(soup_html)
        a_p = self.__retrieve_p_elements(soup_html)
        a_tags = self.__retrieve_article_tags(soup_html)
        a_image = self.__retrieve_article_image(soup_html)
        
        article = Article(a_title, a_p, a_tags, a_image)

        return article

    def __retrieve_article_title(self, soup_html):
        return soup_html.find('title').text

    def __retrieve_p_elements(self, soup_html, get_text=False):
        if get_text:
            return [p.text for p in soup_html.findAll('p')][:-3]

        return soup_html.findAll('p')[:-3]

    def __retrieve_article_tags(self, soup_html):
        return soup_html.findAll("span", class_="cb-element")

    def __retrieve_article_image(self, soup_html):
        img_dict = {}
        img_tag = soup_html.find(class_='wp-caption')

        # Information to retrieve
        img_link = img_tag.a['href']
        img_alt = img_tag.img['alt']
        img_text = img_tag.text

        img_dict['link'] = img_link
        img_dict['alt'] = img_alt
        img_dict['text'] = img_text

        return img_dict