import gdata.youtube
import gdata.youtube.service

class YouTubeExtractor:
	def __init__(self):
		self.yt_service = gdata.youtube.service.YouTubeService()

	def getVideo(self, artist, track):
		query = gdata.youtube.service.YouTubeVideoQuery()
		query.vq = artist + " " + track
		query.orderby = 'relevance'
		query.racy = 'include'
		feed = self.yt_service.YouTubeQuery(query)

		entry = feed.entry[0]
		return {"title": entry.media.title.text, "url": entry.media.player.url} 
