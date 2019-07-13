from mongoengine import Document, EmbeddedDocument, StringField, ListField, EmbeddedDocumentField

class NeuroscienceNewsImage(EmbeddedDocument):
    file_path = StringField(required=True)
    url_link = StringField(required=True)
    caption = StringField(required=True)
    
class NeuroscienceNewsArticle(Document):
    title = StringField(required=True)
    body_text = ListField(StringField(), required=True)
    raw_body_text = ListField(StringField(), required=True)
    tags = ListField(StringField(), required=True)
    image = EmbeddedDocumentField(NeuroscienceNewsImage)
    date_uploaded = StringField(required=True)
    article_url = StringField(required=True)