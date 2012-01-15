from models import *
import logging
import datetime

class UserManager:
	def addUsers(self, data):
		users = []			
		for u in data:
			user = User.all().filter("facebookId = ", u['id']).get()
			if user:
					user.name = u['name']
			else:
				user = User(key_name=u['id'], facebookId = u['id'], name = u['name'])

			try:
				user.access_token = u['access_token']
			except KeyError:
				pass
			
			try:
				logging.debug(u['prefered_artists'])
				for aId in u['prefered_artists']:
					artist = Artist.all().filter("deezerId = ", aId).get()
					user.addPreferedArtist(artist)
			except KeyError:
				pass

			user.put()
			users.append(user)
			
		return users
	
	def getUsers(self, ids=None):
		data = []
		users = User.all()

		if ids:
			users = users.filter("facebookId IN ", ids)
	
		for u in users:
			lastUpdated = datetime.datetime.now() - u.updated
			shouldUpdate = 1 if lastUpdated.days > 1 else 0
			dataUser = {"id": u.facebookId, "name": u.name, "last_updated" : str(lastUpdated), 
			"should_update" : shouldUpdate, "prefered_artists": [Artist.get(a).deezerId for a in u.prefered_artists]}
			data.append(dataUser)
		return data

class ArtistManager:
	def getArtists(self, ids=None):
		data = []
		artists = Artist.all()

		if ids:
			artists = artists.filter("deezerId IN ", ids)

		for a in artists:
			aTracks = []
			for trackKey in a.tracks:
				t = Track.get(trackKey)
				track = {"id": t.deezerId, "name": t.name}
				aTracks.append(track)
			dataArtist = {"id": a.deezerId, "name": a.name, "tracks": aTracks}

			data.append(dataArtist)
		return data
		
	def addArtists(self, data):
		artists = []
		for a in data:
			artist = Artist.all().filter("deezerId = ", a['id']).get()
			if not artist:
				artist = Artist()
			artist.create(a['id'], a['name'])
			artist.put()

			try:
				trackManager = TrackManager()
				tracks = trackManager.addTracks(a['tracks'])
				for t in tracks:
					artist.addTrack(t)
			except KeyError:
				pass

			artists.append(artist)
			artist.put()

		return artists

class TrackManager:
	def getTracks(self):
		data = []
		tracks = Track.all()
		for t in tracks:
			dataTrack = {"id": t.deezerId, "name": t.name}
			if t.artist:
				dataTrack["artistId"] = t.artist.id
			data.append(dataTrack)
		return data

	def addTracks(self, data):
		tracks = []
		for t in data:
			track = Track.all().filter("deezerId = ", t['id']).get()
			if not track:
				track = Track()
			track.create(t['id'], t['name'])
			tracks.append(track)

		for t in tracks:
			t.put()

		return tracks
