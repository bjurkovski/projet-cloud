from google.appengine.ext import db

# * Type Quick Reference: 
# db.DateTimeProperty(auto_now_add=True)
# db.BooleanProperty()
# db.ReferenceProperty(_otherType_)
# db.IntegerProperty()

class User(db.Model):
	facebookId = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	updated = db.DateTimeProperty(auto_now=True)
	access_token = db.StringProperty()
	prefered_artists = db.ListProperty(db.Key)

	def create(self, uid, name):
		self.facebookId = uid
		self.name = name

	def addPreferedArtist(self, artist):
		if not artist.key() in self.preferedArtists:
			self.preferedArtists.append(artist)
			artist.likedBy.append(self)

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
		if not track.key() in self.tracks:
			self.tracks.append(track.key())
			track.artist = self

class Track(db.Model):
	deezerId = db.StringProperty()
	name = db.StringProperty()
	artist = db.ReferenceProperty(Artist)

	def create(self, sid, name):
		self.deezerId = sid
		self.name = name
