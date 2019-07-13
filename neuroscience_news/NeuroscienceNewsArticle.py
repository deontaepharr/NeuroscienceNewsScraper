class NeuroscienceNewsArticle:
    
    def __init__(self, title, body_text, raw_body_text, tags, image, date_uploaded, article_url):
        self.title = title
        self.body_text = body_text
        self.raw_body_text = raw_body_text
        self.tags = tags
        self.image = image
        self.date_uploaded = date_uploaded
        self.article_url = article_url