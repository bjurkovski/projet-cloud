window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
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
							showTopArtists(user.topArtists);
						}
					}
				}
			});
		}
	});
}

function showTopArtists(artists) {
	document.getElementById('face').innerHTML += "<br/>Top Artists<br/>";
	for(var i=0; i<artists.length; i++) {
		document.getElementById('face').innerHTML += artists[i].name + "<br/>";
		document.getElementById('face').innerHTML += "<div id='tracks-" + artists[i].id + "'>Loading...</div><br/>";
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
				for(var j=0; j<json.data[i].tracks.length; j++) {
					if(j>0) toPrint += ", ";
					toPrint += json.data[i].tracks[j].name;
				}
				toPrint += "<br/>";
			}
			document.getElementById('tracks-'+artistId).innerHTML = toPrint;
		}
	});
}

