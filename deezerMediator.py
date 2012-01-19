from django.utils import simplejson as json

import urllib
import string

class DeezerMediator:

	API_URL = 'http://api.deezer.com/'
	API_VERSION = '2.0'

	def getArtist(self, query):
		page = urllib.urlopen(DeezerMediator.API_URL + DeezerMediator.API_VERSION + '/search/artist?q=' + query)			
		content = json.loads(page.read())
		
		query = string.split(string.lower(query))
		bestSimilarity = -1
		bestSkew = 9999
		for artist in content['data']:
			similarity = 0
			skew = 0
			a = string.split(string.lower(artist['name']))
			for word in a:
				if any(word in s for s in query): 
					similarity +=1
				else:
					skew += len(word)
			if similarity >= bestSimilarity and skew <= bestSkew :
				bestSimilarity = similarity
				bestSkew = skew
				selected = artist
		return selected
		
	def getTracks(self, artist):
		songs = []

		page = urllib.urlopen(DeezerMediator.API_URL + DeezerMediator.API_VERSION + '/search?q=' + artist['name'])
		content = json.loads(page.read())
		
		for song in content['data']:
			if song['artist']['id'] == artist['id']:
				songs.append(song)
		
		return songs
