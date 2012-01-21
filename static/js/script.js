window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true,  // parse XFBML
		oauth	   : true
	});

	main();

	FB.Event.subscribe("auth.authResponseChange", function(response) {
         // Reload the same page
         window.location.reload();
	});
};

// Load the SDK Asynchronously
(function(d){
	var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
	js = d.createElement('script'); js.id = id; js.async = true;
	js.src = "//connect.facebook.net/en_US/all.js";
	d.getElementsByTagName('head')[0].appendChild(js);
}(document));

var LOADING_GIF = "/static/img/loading.gif";
var LOADING_IMG = "<img src='" + LOADING_GIF + "' style='vertical-align: center;' alt='Loading...'/>";

function main() {
	FB.getLoginStatus(function(response) {
	  if (response.status === 'connected') {
			var uid = response.authResponse.userID;

			$.ajax({url: "/user/" + uid,
				type: 'GET',
				dataType: 'json',
				success: function(json) {
					if(json.status == "OK") {
						var user = json.data[0];
						document.getElementById('face').innerHTML += "<br/>[Debug: ";
						if(user.needsUpdate) {
							document.getElementById('face').innerHTML += " user needs to be updated]<br/>";
							document.getElementById('face').innerHTML += "<div id='artists'>"
												+ LOADING_IMG + " Loading..."
												+ "</div>";
							$.ajax({url: "/topArtists",
									type: 'GET',
									dataType: 'json',
									success: function(artistsJson) {
										showTopArtists(artistsJson.data);
									}
							});
						}
						else {
							document.getElementById('face').innerHTML += " user doesn't needs to be updated]<br/>";
							document.getElementById('face').innerHTML += "<div id='artists'>"
												+ LOADING_IMG + " Loading..."
												+ "</div>";
							showTopArtists(user.topArtists);
						}
					}
				}
			});
		}
	});
}

function showTopArtists(artists) {
	document.getElementById('artists').innerHTML = "<h1>Top Artists</h1>";
	for(var i=0; i<artists.length; i++) {
		var artistBox = "<div class='box'><h1>" + artists[i].name + "</h1>";
		artistBox += "<div id='tracks-" + artists[i].id + "'>" + LOADING_IMG + "Loading...</div></div>";
		document.getElementById('artists').innerHTML += artistBox;
		showTracks(artists[i].id);
	}
}

function showTracks(artistId) {
	$.ajax({url: "/track/artistId/" + artistId,
		type: 'GET',
		dataType: 'json',
		success: function(json) {
			var toPrint = "";
			for(var i=0; i<json.data.length; i++) {
				var numTracks = json.data[i].tracks.length;
				if(numTracks > 5) numTracks = 5; 
				for(var j=0; j<numTracks; j++) {
					toPrint += "<li>" + json.data[i].tracks[j].name + "</li>";
				}
			}
			document.getElementById('tracks-'+artistId).innerHTML = "<ul>" + toPrint + "</ul>";
		}
	});
}


