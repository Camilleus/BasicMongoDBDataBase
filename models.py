from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, BooleanField

class Author(Document):
    fullname = StringField(required=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent_email = BooleanField(default=False)
    phone_number = StringField()
    preferred_method = StringField(choices=["email", "sms"])