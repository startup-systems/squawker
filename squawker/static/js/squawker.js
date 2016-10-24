function squawk() {
	var squawkComposer = $( "#squawkComposer" );
	var body = {
		"text": squawkComposer.val(),
		"time": new Date().getTime(),
		"username": "trvslhlt"
	};
	$.ajax({
		type: "POST",
		url: "/squawk",
		data: JSON.stringify(body),
		contentType: "application/json; charset=utf-8",
		success: function(data) { alert(data); },
		failure: function(err) { alert(err); }
	});
}

function getAllSquawks() {
	$.ajax({
		type: "GET",
		url: "/squawks",
		dataType: "html",
		success: function(html) {
			$( "#feed-container" ).replaceWith(html);
		},
		failure: function(err) { alert(err); }
	});
}

getAllSquawks();
