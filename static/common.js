function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	    var cookie = jQuery.trim(cookies[i]);
	    // Does this cookie string begin with the name we want?
	    if (cookie.substring(0, name.length + 1) == (name + '=')) {
		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		break;
	    }
	}
    }
    return cookieValue;
}

function getCsrfCookie() {
    return getCookie('frryd_csrf_cookie');
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken",  getCsrfCookie());
        }
    }
});

function showAjaxFailure(data) {
    result = $.parseJSON(data.responseText);
    n = noty({
	text: result.message,
        type: 'error',
        dismissQueue: true,
        layout: 'topRight',
	timeout: 3800
    });
}

function is_mobile() {
    return $(window).width() < 767;
}

function is_short() {
    return $(window).height() < 350;
}

function fill_element(resize_element_id, elements) {
    var win_width = $(window).width();
    if (is_mobile()) {
	var win_height = $(window).height();
	var other_height = 0;
	for (var i = 0; i < elements.length; i++) {
	  other_height += $("#" + elements[i]).height();
	}
	$("#" + resize_element_id).height(win_height - other_height);
    } else {
	$("#" + resize_element_id).height(500);
    }
};
