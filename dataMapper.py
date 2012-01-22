from deezerExtractor import *
from facebookExtractor import *
from youtubeExtractor import *

class DataMapper:
	def __init__(self):
		self.facebookExtractor = FacebookExtractor()
		self.deezerExtractor = DeezerExtractor()
		self.youtubeExtractor = YouTubeExtractor()

	def getTracks(self, artist):
		tracks = self.deezerExtractor.getTracks(artist)
		tracksDict = []
		for t in tracks:
			video = self.youtubeExtractor.getVideo(artist["name"], t["title"])
			tDict =  {
				"id": t["id"],
				"name": t["title"],
				"deezerUrl": t["link"],
				"videoUrl": video["url"]
			}
			try: tDict["deezerRank"] = t["rank"]
			except KeyError: pass
			try: tDict["previewUrl"] = t["preview"]
			except KeyError: pass
			tracksDict.append(tDict)
		return tracksDict

	def getFriendsMusic(self, numResults, cookies):
		topArtists = self.facebookExtractor.getTopFriendsMusic(numResults, cookies)
		artists = []
		for artist in topArtists:
			artist = self.deezerExtractor.getArtist(artist["artist"])
			try: link = artist["link"]
			except KeyError: link = None
			try: picture = artist["picture"]
			except KeyError: picture = None
			artists.append({
				"id": artist["id"],
				"name": artist["name"],
				"deezerUrl": link,
				"pictureUrl": picture
			})
		return artists
