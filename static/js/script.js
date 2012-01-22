window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
		channelUrl : 'channel.html',
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true,  // parse XFBML
		oauth	   : true
	});

	main();
};

// Load the SDK Asynchronously
(function(d){
	var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
	js = d.createElement('script'); js.id = id; js.async = true;
	js.src = "//connect.facebook.net/en_US/all.js";
	d.getElementsByTagName('head')[0].appendChild(js);
}(document));

var LOADING_ICON = "/static/img/loading.gif";
var MUSIC_ICON = "/static/img/music.png";
var YOUTUBE_ICON = "/static/img/youtube.png";
var LOADING_IMG = "<img src='" + LOADING_ICON + "' style='vertical-align: middle;' alt='Loading...'/>";
var MUSIC_IMG = "<img src='" + MUSIC_ICON + "' style='vertical-align: middle;' width='24px' alt='Listen'/>";
var YOUTUBE_IMG = "<img src='" + YOUTUBE_ICON + "' style='vertical-align: middle;' width='24px' alt='Watch video'/>";

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
/*
						document.getElementById('face').innerHTML += "<br/>[Debug: user ";
						if(!user.needsUpdate) document.getElementById('face').innerHTML += "doesn't ";
						document.getElementById('face').innerHTML += "needs to be updated]<br/>";
*/

						document.getElementById('face').innerHTML += "<h2>Your friend's top artists are...</h2>";
						if(user.needsUpdate) {
							document.getElementById('face').innerHTML += "<div id='artists'>"
												+ LOADING_IMG + " Loading..."
												+ "</div><div id='artists'></div>";
							$.ajax({url: "/topArtists",
									type: 'GET',
									dataType: 'json',
									success: function(artistsJson) {
										showTopArtists(artistsJson.data);
									}
							});
						}
						else {
							document.getElementById('face').innerHTML += "<div id='loading'>"
												+ LOADING_IMG + " Loading..."
												+ "</div><div id='artists'></div>";
							showTopArtists(user.topArtists);
						}
					}
				}
			});
		}
	});
}

function showTopArtists(artists) {
	document.getElementById('artists').innerHTML = "";
	for(var i=0; i<artists.length; i++) {
		var artistBox = "<div class='box'><h1>" + artists[i].name + "</h1>";
		artistBox += "<span class='column watermark'>" + (i+1) + "</span>";
		artistBox += "<span class='column content'><span id='tracks-" + artists[i].id + "'>" + LOADING_IMG + " Loading...</span></span>";
		artistBox += "</div>";
		document.getElementById('artists').innerHTML += artistBox;
		showTracks(artists[i].id);
	}
	document.getElementById('loading').innerHTML = "";
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
					var track = json.data[i].tracks[j]
					toPrint += "<li>" + track.name + " ";
					if(track.deezerUrl)
						toPrint += "<a href='" + track.deezerUrl + "' target='_blank'>" + MUSIC_IMG + "</a> ";
					if(track.videoUrl)
						toPrint += "<a href='" + track.videoUrl + "' target='_blank'>" + YOUTUBE_IMG + "</a>";
					toPrint += "</li>";
				}
			}
			document.getElementById('tracks-'+artistId).innerHTML = "<ul>" + toPrint + "</ul>";
		}
	});
}

function after_login_button() {
    FB.getLoginStatus(function(response) {
        if (response.status=="connected") {
            window.location.reload();
        }
		else
			window.location.reload();
    }, true);
}


