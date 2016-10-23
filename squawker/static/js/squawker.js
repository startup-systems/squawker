
function squawk() {
	$(function () {
		var squawkComposer = $("#squawkComposer");
		var text = squawkComposer.val();
		var date = new Date();
		var time = date.getTime();
		var username = "trvslhlt";
		var body = {
			"text": text,
			"time": time,
			"username": username
		};
		console.log(JSON.stringify(body));
	});
	
}
