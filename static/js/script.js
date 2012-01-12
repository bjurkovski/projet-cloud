window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
//		channelUrl : '/channel.html', // Channel File
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true  // parse XFBML
	});

	dbTest();
	document.getElementById("test").innerHTML = "will try to login...";
	//deezerSearchArtist("oasis");
	FB.getLoginStatus(function(response) {
		if (response.status === 'connected') {
			// the user is logged in and connected to your
			// app, and response.authResponse supplies
			// the user's ID, a valid access token, a signed
			// request, and the time the access token 
			// and signed request each expire
			var uid = response.authResponse.userID;
			var accessToken = response.authResponse.accessToken;
			document.getElementById("test").innerHTML = "conectado!";
		} else if (response.status === 'not_authorized') {
			// the user is logged in to Facebook, 
			//but not connected to the app
			document.getElementById("test").innerHTML = "nao autorizado!";
		} else {
			// the user isn't even logged in to Facebook.
			document.getElementById("test").innerHTML = "nao logado!";
		}
	});
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

function dbTest() {
	var artistJson = new Object;
	artistJson.data = new Array;

	var artist = new Object;
	artist.id = "456";
	artist.name = "Outro nome :D";
	artistJson.data.push(artist);

	var JSONstring = $.toJSON(artistJson);

	$.ajax({url: "/artist",
		type: 'POST',
		data: "json=" + JSONstring,
		dataType: 'json',
		success: function(json) {
			if(json.status == "ERROR")
				alert("Error creating a new artist...");
		}
	});
}

function deezerSearchArtist(artistName) {
	$.ajax({url: DEEZER_API_URL + DEEZER_API_VERSION + "/search/artist?q=" + artistName,
		type: 'GET',
		dataType: 'json',
		success: function(json) {
			if(json.data.length > 0) {
				document.getElementById("test").innerHTML = "Artist: " + json.data[0].name;
			}
		}
	});
}

function deezerSearch(query) {
	document.getElementById("test").innerHTML = "Will search " + query + "...";
	$.ajax({url: DEEZER_API_URL + DEEZER_API_VERSION + "/search?q=" + query,
		type: 'GET',
		dataType: 'json',
		success: function(json) {
			var size = json.data.length;
			if(size > 5) size = 5;
			var tracks = "";

			for(var i=0; i<size; i++) {
				if(i>0) tracks += ", ";
				tracks += json.data[i].title;
			}
			document.getElementById("test").innerHTML = "Searched '" + query + "' at Deezer. Results: " + tracks;
		}
	});
};
