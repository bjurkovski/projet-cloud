from google.appengine.ext import db

# * Type Quick Reference: 
# db.DateTimeProperty(auto_now_add=True)
# db.BooleanProperty()
# db.ReferenceProperty(_otherType_)
# db.IntegerProperty()

class User(db.Model):
	id = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty(auto_now=True)
	profile_url = db.StringProperty(required=True)
	access_token = db.StringProperty(required=True)
	preferedArtists = db.ListProperty(db.Key)
	friends = db.ListProperty(db.Key)

	def create(self, uid, name):
		self.facebookId = uid
		self.name = name

	def addPreferedArtist(self, artist):
		self.preferedArtists.append(artist)
		artist.likedBy.append(self)
		artist.put()

	def addFriend(self, friend): 
		self.friends.append(friend)
		friend.friends.append(self)
		friend.put()

	def __str__(self):
		return self.name

class Artist(db.Model):
	deezerId = db.StringProperty()
	name = db.StringProperty()
	tracks = db.ListProperty(db.Key)
	likedBy = db.ListProperty(db.Key)

	def create(self, aid, name):
		self.deezerId = aid
		self.name = name

	def addTrack(self, track):
		self.tracks.append(song)
		track.artist = self
		track.put()

class Track(db.Model):
	deezerId = db.StringProperty()
	name = db.StringProperty()
	artist = db.ReferenceProperty(Artist)

	def create(self, sid, name):
		self.deezerId = sid
		self.name = name
