from google.appengine.ext import db

# * Type Quick Reference: 
# db.DateTimeProperty(auto_now_add=True)
# db.BooleanProperty()
# db.ReferenceProperty(_otherType_)
# db.IntegerProperty()

class Artist(db.Model):
	name = db.StringProperty()

class Person(db.Model):
	name = db.StringProperty()
	preferedArtists = db.ListProperty(db.Key)
