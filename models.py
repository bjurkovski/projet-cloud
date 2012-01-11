from google.appengine.ext import db

# * Type Quick Reference: 
# db.DateTimeProperty(auto_now_add=True)
# db.BooleanProperty()
# db.ReferenceProperty(_otherType_)
# db.IntegerProperty()

class User(db.Model):
	name = db.StringProperty()
	preferedArtists = db.ListProperty(db.Key)

class Artist(db.Model):
	deezerId = db.IntegerProperty()
	name = db.StringProperty()
	songs = db.ListProperty(db.Key)

class Song(db.Model):
	deezerId = db.IntegerProperty()
	name = db.StringProperty()
