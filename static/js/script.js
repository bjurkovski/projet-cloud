window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true,  // parse XFBML
		oauth	   : true
	});

	document.getElementById("test").innerHTML = "will try to login...";
	savePreferedArtists();

	// Additional initialization code here
};

// Load the SDK Asynchronously
(function(d){
	var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
	js = d.createElement('script'); js.id = id; js.async = true;
	js.src = "//connect.facebook.net/en_US/all.js";
	d.getElementsByTagName('head')[0].appendChild(js);
}(document));

var DEEZER_API_URL = "http://api.deezer.com/";
var DEEZER_API_VERSION = "2.0";
var asyncCallsReturn = new Array;

function searchAddArtist(query, callId) {
	$.ajax({url: DEEZER_API_URL + DEEZER_API_VERSION + "/search?q=" + query,
		type: 'GET',
		dataType: 'json',
		success: function(songsJson) {			
			$.ajax({url: DEEZER_API_URL + DEEZER_API_VERSION + "/search/artist?q=" + query,
				type: 'GET',
				dataType: 'json',
				success: function(artistsJson) {
					if(artistsJson.data.length > 0) {
						var json = new Object;
						json.data = new Array;
						var artist = new Object;
						artist.id = artistsJson.data[0].id;
						artist.name = encodeURI(artistsJson.data[0].name.replace("&", "and"));
						artist.tracks = new Array;
						for(var i=0; i< songsJson.data.length; i++){
							if(songsJson.data[i].artist.id == artistsJson.data[0].id) {				 
								var track = new Object;
								track.id = songsJson.data[i].id; 
								track.name = encodeURI(songsJson.data[i].title.replace("&", "and"));
								artist.tracks.push(track);
							}
						}
						json.data.push(artist);
						sendArtist(json, callId);
					}
				}
			});
		}
	});
};

function sendArtist(json, callId) {
	var id = json.data[0].id 
	json = $.toJSON(json)
	$.ajax({url: "/artist",
				type: 'POST',
				data: "json=" + json,
				dataType: 'json',
				success: function(jsonAnswer) {
//					alert(callId);
//					asyncCallsFinished[callId] = 1;
					asyncCallsReturn[callId] = id;
					if(jsonAnswer.status == "ERROR")
						alert("Error creating a new artist...");
				}
	});
}

function sendUser(json) {
	var finishedCalls = true;
	for(var i=0; i<asyncCallsReturn.length; i++) {
		if(asyncCallsReturn[i] == null) {
			finishedCalls = false;
			break;
		}
	}

	if(finishedCalls) {
		var str = "";
		for(var i=0; i<asyncCallsReturn.length; i++) {
			str += asyncCallsReturn[i] + ", ";
		}
		json.data[0].prefered_artists = asyncCallsReturn;
		json = $.toJSON(json);
		$.ajax({url: "/user",
					type: 'POST',
					data: "json=" + json,
					dataType: 'json',
					success: function(jsonAnswer) {
						if(jsonAnswer.status == "ERROR")
							alert("Error creating (or updating) a user...");
					}
		});
	}
	else {
		setTimeout(function() { sendUser(json); }, 50);
	}
}

function savePreferedArtists(){
	FB.getLoginStatus(function(response) {
	  if (response.status === 'connected') {
			var uid = response.authResponse.userID;

			$.ajax({url: "/user/" + uid,
					type: 'GET',
					dataType: 'json',
					success: function(users) {
						var shouldUpdate = true;
						if(users.data.length > 0) {						
							shouldUpdate = users.data[0].should_update;
						}
						if (shouldUpdate){
							document.getElementById('face').innerHTML += "Finding your friends artists..."
							searchFriendsArtists();
						}
						else {
							document.getElementById('face').innerHTML += "You have updated Recently your artists... ";
						}
					}
				});
	  } else if (response.status === 'not_authorized') {
	  } else {
	  }
	 });
}

function searchFriendsArtists() {
	FB.getLoginStatus(function(response) {
	  if (response.status === 'connected') {
		var uid = response.authResponse.userID;
		var accessToken = response.authResponse.accessToken;
		var myself = FB.Data.query('select name, uid from user where uid={0}', uid);
	 	
		document.getElementById('face').innerHTML += "Requesting data from Facebook ... ";

		var friends = FB.Data.query("SELECT uid2 FROM friend WHERE uid1={0}", uid);
		var friendsMusic = FB.Data.query("SELECT music FROM user WHERE uid IN (select uid2 from {0})", friends);

		FB.Data.waitOn([myself, friends, friendsMusic], function() {
			var artists = [];
			FB.Array.forEach(friendsMusic.value, function(row) {
				if(row.music != "") {
					var musics = row.music.split(",")
					for(var j=0; j<musics.length; j++) {
						var aName = musics[j].replace("&", "and");
						var found = false;
						for(var k=0; k<artists.length; k++) {
							if(artists[k][0] == aName) {
								artists[k][1]++;
								found = true;
							}
						}
						if(!found) artists.push([aName, 1]);
					}
				}
		   });

			artists.sort(function(a, b) {
				a = a[1];
				b = b[1];
				return a > b ? -1 : (a < b ? 1 : 0);
			});

			var json = new Object;
			json.data = new Array;
			var user = new Object;
			user.id = uid;
			user.name = myself.value[0].name;
			user.access_token = accessToken;
			user.prefered_artists = new Array;

			var size = artists.length;
			if(size > 5) size = 5;

			asyncCallsReturn = new Array;
			for(var i=0; i<size; i++) {
				asyncCallsReturn.push(null);
			}

			for(var i=0; i<size; i++) {
				searchAddArtist(artists[i][0], i);
			}

			json.data.push(user);
			sendUser(json);
		});
	  } else if (response.status === 'not_authorized') {
	  } else {
	  }
	 });
 }


