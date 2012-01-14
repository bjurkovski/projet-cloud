from models import *

class ArtistManager:
	def getArtists(self, ids=None):
		data = []
		artists = Artist.all()

		if ids:
			artists = artists.filter("deezerId IN", ids)

		for a in artists:
			tracks = Track.all().filter("artist = ", a)
			aTracks = []
			for t in tracks:
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

			try:
				trackManager = TrackManager()
				tracks = trackManager.addTracks(a['tracks'])['tracks']
				for t in tracks:
					artist.addTrack(t)
			except KeyError:
				pass

			artists.append(artist)
		for a in artists:
			a.put()

		return artists

class TrackManager:
	def getTracks(self):
		data = []
		tracks = Track.all()
		for t in tracks:
			dataTrack = {"id": t.deezerId, "name": t.name, "artistId": t.artist.id}
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
