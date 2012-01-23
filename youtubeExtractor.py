import gdata.youtube
import gdata.youtube.service
import urllib
import unicodedata

class YouTubeExtractor:
	def __init__(self):
		self.yt_service = gdata.youtube.service.YouTubeService()

	def getVideo(self, artist, track):
		query = gdata.youtube.service.YouTubeVideoQuery()
		query.vq =  unicodedata.normalize('NFKD', artist + " " + track).encode('ascii','ignore')
		query.orderby = 'relevance'
		query.racy = 'include'
		feed = self.yt_service.YouTubeQuery(query)

		if len(feed.entry) == 0:
			return None

		entry = feed.entry[0]
		return {"title": entry.media.title.text, "url": entry.media.player.url} 
