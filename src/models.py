
import mongoengine as db
import bson


class User(db.Document):

    id = db.ObjectIdField(primary_key=True, default=bson.ObjectId)
    username = db.StringField()
    password = db.StringField()
    
    meta = {
        'indexes': [
            {
                'fields': ['username'],
                'unique': True,
            }
        ],
        'collection': 'user',
    }
