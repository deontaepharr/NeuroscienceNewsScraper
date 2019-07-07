class NeuroscienceNewsArticle:
    
    def __init__(self, title, body_text, raw_body_text, tags, image, date_uploaded):
        self.title = title
        self.body_text = body_text
        self.raw_body_text = raw_body_text
        self.tags = tags
        self.image = image
        self.date_uploaded = date_uploaded
        
    def __str__(self):
        return "Article -- (Title: {},\n\nBody Text: {},\n\nTags: {},\n\nImage: {})" \
                .format(self.title, self.body_text, self.tags, self.image)
