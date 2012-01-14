window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true,  // parse XFBML
		oauth	   : true
	});

	document.getElementById("test").innerHTML = "will try to login...";
	searchFriendsMusics();
	deezerSearch("eminem");

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

function deezerSearch(query) {
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
						json.data[0].artist = new Object;
						json.data[0].artist.id = artistsJson.data[0].id;
						json.data[0].artist.name = artistsJson.data[0].name;
						for(var i=0; i< songsJson.data.length; i++){
							if(songsJson.data[i].artist.id == artistsJson.data[0].id) {				 
								json.data[0].artist.tracks[i] = new Object;
								json.data[0].artist.tracks[i].id = songsJson.data[i].id; 
								json.data[0].artist.tracks[i].name = songsJson.data[i].title;
							}
						}
						sendArtist($.toJSON(json));
					}
				}
			});
		}
	});
};

function sendArtist(json) {
	$.ajax({url: "/artist",
				type: 'POST',
				data: "json=" + json,
				dataType: 'json',
				success: function(jsonAnswer) {
					if(jsonAnswer.status == "ERROR")
						alert("Error creating a new artist...");
				}
	});
}

function writeObj(obj, message) {
  if (!message) { message = obj; }
  var details = "*****************" + "\n" + message + "\n";
  var fieldContents;
  for (var field in obj) {
    fieldContents = obj[field];
    if (typeof(fieldContents) == "function") {
      fieldContents = "(function)";
    }
    details += "  " + field + ": " + fieldContents + "\n";
  }
  console.log(details);
}


function searchFriendsMusics() {
	FB.getLoginStatus(function(response) {
	  if (response.status === 'connected') {
		document.getElementById('face').innerHTML += "Connected! ";
		// the user is logged in and connected to your
		// app, and response.authResponse supplies
		// the user's ID, a valid access token, a signed
		// request, and the time the access token 
		// and signed request each expire
		var uid = response.authResponse.userID;
		var accessToken = response.authResponse.accessToken;
		var query = FB.Data.query('select name, uid from user where uid={0}', uid);
	 	query.wait(function(rows) {
			console.log('Your name is ' + rows[0].name);
	 	});

		document.getElementById('face').innerHTML += "Requesting data from Facebook ... ";

		var friends = FB.Data.query("SELECT uid2 FROM friend WHERE uid1={0}", uid);
		var friendsMusic = FB.Data.query("SELECT music FROM user WHERE uid IN (select uid2 from {0})", friends);

		FB.Data.waitOn([friends, friendsMusic], function() {
			var count = 0;
			var artists = [];
			FB.Array.forEach(friendsMusic.value, function(row) {
				var musics = row.music.split(",")
				for(var j=0; j<musics.length; j++) {
					var aName = musics[j];
					var found = false;
					for(var k=0; k<artists.length; k++) {
						if(artists[k][0] == aName) {
							artists[k][1]++;
							found = true;
						}
					}
					if(!found) artists.push([aName, 1]);
				}
				count++;
		   });

			artists.sort(function(a, b) {
				a = a[1];
				b = b[1];
				return a > b ? -1 : (a < b ? 1 : 0);
			});

			var size = artists.length;
			if(size > 5) size = 5;

			var results = "";

			results += "<ul>";
			results += "<li class='title'>Friends top artists:</li>";
			for(var i=0; i<size; i++)
				results += "<li>" + artists[i][0] + ": " + artists[i][1] + " friends</li>";
			results += "</ul>";

			document.getElementById('face').innerHTML += results;
		});
	  } else if (response.status === 'not_authorized') {
		//alert("nao autorizado");
		// the user is logged in to Facebook, 
		//but not connected to the app
	  } else {
		//alert("nao logado");
		// the user isn't even logged in to Facebook.
	  }
	 });
 }


