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

	def addArtists(self, user, artists):
		if user:
			for artist in artists:
				user.addPreferedArtist(artist)
			user.put()
			return user
		else:
			return None
	
	def getUsers(self, ids=None):
		users = User.all().filter("facebookId IN ", ids) if ids else User.all()
		return users

class ArtistManager:
	def getArtists(self, ids=None):
		artists = Artist.all().filter("deezerId IN ", ids) if ids else Artist.all()
		return artists

	def addTracks(self, artist, tracks):
		if artist:
			for track in tracks:
				artist.addTrack(track)
			artist.put()
			return artist
		else:
			return None
		
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

			try: artist.deezerUrl = a['deezerUrl']
			except KeyError: pass

			try: artist.pictureUrl = a['pictureUrl']
			except KeyError: pass

			artists.append(artist)
			artist.put()

		return artists

class TrackManager:
	def getTracks(self, ids=None):
		data = []
		tracks = Track.all()
		for t in tracks:
			data.append(t)
		return data

	def addTracks(self, data):
		tracks = []
		for t in data:
			track = Track.all().filter("deezerId = ", t['id']).get()
			if not track:
				track = Track()
			track.create(t['id'], t['name'])
			tracks.append(track)

			try: track.deezerUrl = t['deezerUrl']
			except KeyError: pass

			try: track.deezerRank = t['deezerRank']
			except KeyError: pass

			try: track.previewUrl = t['previewUrl']
			except KeyError: pass

			try: track.videoUrl = t['videoUrl']
			except KeyError: pass

		for t in tracks:
			t.put()

		return tracks
