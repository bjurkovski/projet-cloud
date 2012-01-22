import facebook
import yaml
from django.utils import simplejson as json

class FacebookExtractor:
	FB_APP_ID = ""
	FB_APP_SECRET = ""

	def __init__(self):
		data = yaml.load(file("facebook.yaml", "r"))
		FacebookExtractor.FB_APP_ID = str(data["app_id"])
		FacebookExtractor.FB_APP_SECRET = str(data["app_secret"])

	def getGraph(self, cookies=None):
		cookie = self.getCurrentUserCookie(cookies)
		if not cookie:
			return facebook.GraphAPI()
		return facebook.GraphAPI(cookie["access_token"])

	def getCurrentUserCookie(self, cookies=None):
		if not cookies:
			return None
		return facebook.get_user_from_cookie(cookies, FacebookExtractor.FB_APP_ID, FacebookExtractor.FB_APP_SECRET)

	def getTopFriendsMusic(self, limit=5, cookies=None):
		requests = [
			{"method": "POST",
			 "relative_url": "method/fql.query?query=SELECT+music+FROM+user+WHERE+uid+IN+(SELECT+uid2+FROM+friend+WHERE+uid1=me())"
			}
		]

		data = self.getGraph(cookies).request("", post_args={
			"batch": json.dumps(requests)
		})

		musicJson = json.loads(data[0]["body"])

		allArtists = {}
		for musicData in musicJson:
			artists = musicData["music"].split(",")
			for artist in artists:
				if artist != "":
					a = artist.strip()
					try:
						allArtists[a] += 1
					except KeyError:
						allArtists[a] = 0


		orderedArtistKeys = sorted(allArtists, key=lambda key: allArtists[key])
		orderedArtistKeys.reverse()
		orderedArtists = []
		for key in orderedArtistKeys[:min(limit, len(orderedArtistKeys))]:
			orderedArtists.append({"artist": key, "numFriends": allArtists[key]})

		return orderedArtists
