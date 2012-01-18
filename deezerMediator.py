from django.utils import simplejson as json

import urllib

class DeezerMediator:

	API_URL = 'http://api.deezer.com/'
	API_VERSION = '2.0'

	def getArtist(self, query):
		page = urllib.urlopen(DeezerMediator.API_URL + DeezerMediator.API_VERSION + '/search/artist?q=' + query)			
		content = json.loads(page.read())
		
		return content['data'][0]
		
	def getTracks(self, artist):
		songs = []

		page = urllib.urlopen(DeezerMediator.API_URL + DeezerMediator.API_VERSION + '/search?q=' + artist['name'])
		content = json.loads(page.read())
		
		for song in content['data']:
			if song['artist']['id'] == artist['id']:
				songs.append(song)
		
		return songs
