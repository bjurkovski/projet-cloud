window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true,  // parse XFBML
		oauth	   : true
	});
	document.getElementById("test").innerHTML = "will try to login...";
	deezerSearch("eminem");
	searchFriendsMusics();

	// Additional initialization code here
};

// Load the SDK Asynchronously
(function(d){
	var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
	js = d.createElement('script'); js.id = id; js.async = true;
	js.src = "//connect.facebook.net/en_US/all.js";
	d.getElementsByTagName('head')[0].appendChild(js);
}(document));

function deezerSearch(query) {
	document.getElementById("test").innerHTML = "Will search " + query + "...";
	$.ajax({url: "http://api.deezer.com/2.0/search?q=" + query,
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


function searchFriendsMusics() { 

	FB.getLoginStatus(function(response) {
	  if (response.status === 'connected') {
		alert("Conectado");
		// the user is logged in and connected to your
		// app, and response.authResponse supplies
		// the user's ID, a valid access token, a signed
		// request, and the time the access token 
		// and signed request each expire
		var uid = response.authResponse.userID;
		var accessToken = response.authResponse.accessToken;
		var query = FB.Data.query('select name, uid from user where uid={0}',
		                       uid);
	 	query.wait(function(rows) {
		console.log('Your name is ' + rows[0].name);
	 	});

		document.getElementById('face').innerHTML = "Requesting "
		  + "data from Facebook ... ";
		FB.api('me/friends', function(response) {
		    for( i=0; i<response.data.length; i++) {
		      friendId = response.data[i].id;
		      FB.api('/'+friendId+'/music', function(response) {
				for( j=0; j<response.data.length; j++) {
					if(response.data[j].category == "Musician/band") {
						document.getElementById('face').innerHTML += "<br>"+response.data[j].name;
					}
				}
		      });
		    } 
		});
	  } else if (response.status === 'not_authorized') {
		alert("nao autorizado");
		// the user is logged in to Facebook, 
		//but not connected to the app
	  } else {
		alert("nao logado");
		// the user isn't even logged in to Facebook.
	  }
	 });
 }


