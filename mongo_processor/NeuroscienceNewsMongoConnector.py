from .NeuroscienceNewsArticle import NeuroscienceNewsArticle, NeuroscienceNewsImage

from pathlib import Path
from urllib.parse import urlparse

from PIL import Image
import requests

from datetime import datetime

from mongoengine import connect

class NeuroscienceNewsMongoConnector():

    def __init__(self, database_name):
        self.database_name = database_name
        connect(self.database_name)
        
    def save_neuroscience_articles(self, articles):
        if not isinstance(articles, list):
            mongo_article = self.__neuroscience_news_article_for_mongo(articles)
            mongo_article.save()
            
        else:
            mongo_articles = [self.__neuroscience_news_article_for_mongo(article) \
                                for article in articles]
            
            NeuroscienceNewsArticle.objects.insert(mongo_articles)

    def __save_neuro_article_image(self, img_url):
        img_loc_base = Path.cwd().joinpath("data/images")

        if not img_loc_base.exists():
            img_loc_base.mkdir(exist_ok=True)

        # Parse URL for info
        url_parsed = urlparse(img_url)
        file_name = Path(url_parsed.path).name

        # Current Time
        date_time = datetime.now()
        curr_time = date_time.strftime("%m%d%Y_%H%M%S_")

        # Final Path
        img_file_path = img_loc_base.joinpath(curr_time+file_name)

        # Download Image
        n_img = Image.open(requests.get(img_url, stream = True).raw)
        n_img.save(img_file_path)

        return str(img_file_path)

    def __neuroscience_news_article_for_mongo(self, article):

        n_img = NeuroscienceNewsImage(
            file_path = self.__save_neuro_article_image(article.image["link"]),
            url_link = article.image["link"], 
            caption  = article.image["text"]
        )

        n_article = NeuroscienceNewsArticle(
            title = article.title,
            body_text = article.body_text,
            raw_body_text = article.raw_body_text,
            tags = article.tags,
            image = n_img,
            date_uploaded = article.date_uploaded
        )

        return n_article