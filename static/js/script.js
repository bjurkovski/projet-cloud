window.fbAsyncInit = function() {
	FB.init({
		appId      : '173535979414436', // App ID
		channelUrl : '/channel.html', // Channel File
		status     : true, // check login status
		cookie     : true, // enable cookies to allow the server to access the session
		xfbml      : true  // parse XFBML
	});

	document.getElementById("test").innerHTML = "will try to login...";
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
