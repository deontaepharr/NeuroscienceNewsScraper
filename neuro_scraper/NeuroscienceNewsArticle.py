class NeuroscienceNewsArticle:
    
    def __init__(self, title, body_text, tags, image):
        self.title = title
        self.body_text = body_text
        self.tags = tags
        self.image = image
        
    def __str__(self):
        return "Article -- (Title: {},\n\nBody Text: {},\n\nTags: {},\n\nImage: {})" \
                .format(self.title, self.body_text, self.tags, self.image)