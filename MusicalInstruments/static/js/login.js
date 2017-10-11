// START OF GOOGLE LOGIN
$('#googleSignInButton').click(function() {
    auth2.grantOfflineAccess({'redirect_uri': 'postmessage'}).then(signInCallback);
});

function signInCallback(json) {
    console.log('inside callback fuction');
    console.log(json);
    authResult = json;
    if (authResult['code']) {
        // Send the code to the server
        $.ajax({
            type: 'POST',
            url: '/MusicalInstruments/oauth/google/',
            processData: false,
            data: JSON.stringify(authResult, null, '\t'),
            contentType: 'application/json; charset=utf-8',
            success: function(result) {
                // Handle or verify the server response if necessary.
                if (result) {
                    console.log('Login Successful!');
                    window.location.replace(index_categories);
                } else if (authResult['error']) {
                    console.log('There was an error: ' + authResult['error']);
                } else {
                    console.log('Failed to make a server-side call. Check your configuration and console.');
                }
            }
        });
    }
}
// END OF GOOGLE LOGIN

// START OF FACEBOOK LOGIN
window.fbAsyncInit = function() {
    FB.init({
        appId            : '232090517308150',
        autoLogAppEvents : true,
        cookie           : true,
        xfbml            : true,
        version          : 'v2.9'
    });
    FB.AppEvents.logPageView();
};

// Load the SDK asynchronously
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
$('#fbSignInButton').click(function() {
    FB.login(function(response) {
        if (response.status === 'connected') {
            sendTokenToServer();
        } else {
            console.log('FB login not completed');
        }
    }, {scope: 'public_profile,email'});
});

function sendTokenToServer() {
    var access_token = FB.getAuthResponse()['accessToken'];
    console.log(access_token)
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
        console.log('Successful login for: ' + response.name);
        $.ajax({
            type: 'POST',
            url: '/MusicalInstruments/oauth/facebook/',
            processData: false,
            data: JSON.stringify(access_token, null, '\t'),
            // data: access_token,
            contentType: 'application/json; charset=utf-8',
            success: function(result) {
                // Handle or verify the server response if necessary.
                if (result) {
                    console.log('Login Successful!');
                    // $('#result').html('Login Successful!</br>'+ result['token'] + '');
                    window.location.replace(index_categories);
                } else if (authResult['error']) {
                    console.log('There was an error: ' + authResult['error']);
                } else {
                    $('#result').html('Failed to make a server-side call. Check your configuration and console.');
                }
            }
        });
    });
}
// END OF FACEBOOK LOGIN

// Common function to signout
function signOut(provider) {
    if (provider == "google") {
        auth2.signOut().then(function() {
            console.log('User signed out from google');
            window.location.replace(logout_url);
        });
    } else if (provider == "facebook") {
        FB.getLoginStatus(function(response) {
            if (response && response.status === 'connected') {
                FB.logout(function(response) {
                    // document.location.reload();
                    console.log('User signed out from facebook');
                    window.location.replace(logout_url);
                });
            }
        });
    } else {
        console.log('User signed out natively');
        window.location.replace(logout_url);
    }
}
