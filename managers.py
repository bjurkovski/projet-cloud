from models import *

class UserManager:
	def addUsers(self, data):

		users[]			
		for a in data:
			user = User.all().filter("facebookId = ", a['id']).get()
			if not user:
				user = User()
			user.create(a['id'], a['name'])
			user.profile_url = a['profile_url']
			user.access_token = a['access_token']
			for b in a['preferred_artists']:
				user.preferred_artists.append(b)
			users.append(user)
			user.put()
			
			for b in a['friends']:
				friend = User.all().filter("facebookId = ", b['id']).get()
				if not friend:
					friend = User()
				friend.create(b['id'], b['name'])
				user.profile_url = a['profile_url']
				user.access_token = a['access_token']
				for b in a['preferred_artists']:
					user.preferred_artists.append(b)
				friend.addFriend(user)
				friend.put()
				
		return users

class ArtistManager:
	def getArtists(self, ids=None):
		data = []
		artists = Artist.all()

		if ids:
			artists = artists.filter("deezerId IN", ids)

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
