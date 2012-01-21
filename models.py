from google.appengine.ext import db
import datetime

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

	def addPreferedArtist(self, artist):
		if not artist.key() in self.prefered_artists:
			self.prefered_artists.append(artist.key())
			artist.likedBy.append(self)

	def toDict(self):
		lastUpdated = datetime.datetime.now() - self.updated
		needsUpdate = True if (lastUpdated.days > 1) or (len(self.prefered_artists) == 0) else False
		topArtists = [a.toDict() for a in Artist.get(self.prefered_artists)]
		data = {
			"id": self.facebookId,
			"name": self.name,
			"needsUpdate": needsUpdate,
			"topArtists": topArtists
		}
		return data

	def __str__(self):
		return self.name

class Artist(db.Model):
	deezerId = db.StringProperty()
	name = db.StringProperty()
	tracks = db.ListProperty(db.Key)
	likedBy = db.ListProperty(db.Key)
	updated = db.DateTimeProperty(auto_now=True)
	deezerUrl = db.TextProperty()
	pictureUrl = db.TextProperty()

	def create(self, aid, name):
		self.deezerId = aid
		self.name = name

	def addTrack(self, track):
		if not track.key() in self.tracks:
			self.tracks.append(track.key())
			track.artist = self

	def toDict(self):
		data = {
			"id": self.deezerId,
			"name": self.name,
			"deezerUrl": self.deezerUrl,
			"pictureUrl": self.pictureUrl,
			"needsUpdate": self.needsUpdate()
		}
		return data
		
	def needsUpdate(self):
		lastUpdated = datetime.datetime.now() - self.updated
		return True if (lastUpdated.days > 1) or (len(self.tracks) == 0) else False 

class Track(db.Model):
	deezerId = db.StringProperty()
	name = db.StringProperty()
	artist = db.ReferenceProperty(Artist)
	deezerUrl = db.TextProperty()
	deezerRank =db.IntegerProperty()
	previewUrl = db.TextProperty()

	def create(self, sid, name):
		self.deezerId = sid
		self.name = name

	def toDict(self):
		data = {
			"id": self.deezerId,
			"name": self.name,
			"deezerUrl": self.deezerUrl,
			"deezerRank": self.deezerRank,
			"previewUrl": self.previewUrl
		}
		return data
