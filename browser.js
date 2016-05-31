const TIME_INTERVAL = 1000;
var lastStateOnline = null;

function isFriendOnline(friend_slug) {
	// list of friends with chatbox open on browser
	var chat_open_friends = document.querySelectorAll(".titlebarText.fixemoji");

	for (var i = chat_open_friends.length - 1; i >= 0; i--) {
		if (chat_open_friends[i].href == "https://www.facebook.com/" + friend_slug) {
			var friend = chat_open_friends[i];
			if (friend.parentNode.parentNode.querySelector('img').alt == "Online") {
				return true;
			} else {
				return false;
			}
		}
	}
};

function checkPresencePeriodically(friend_slug) {
	setInterval(function() {
		var presence = isFriendOnline(friend_slug);
		if (presence != lastStateOnline) {
			console.log(friend_slug + ": " +
				new Date().toISOString() + ": " + presence)
			lastStateOnline = presence;
		}
	}, TIME_INTERVAL);
}

checkPresencePeriodically("USERNAME_GOES_HERE");