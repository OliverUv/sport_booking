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

function resize_map(map_element_id, related_size_element) {
    var win_width = $(window).width();
    if (win_width < 767) {
	var win_height = $(window).height();
	var other_height = $("#" + related_size_element).height();
	$("#" + map_element_id).height(win_height - other_height);
    } else {
	$("#" + map_element_id).height(500);
    }
};

function initializeMap(map_element_id, latitude, longitude) {
    var mapOptions = {
	center: new google.maps.LatLng(latitude, longitude),
	zoom: 16,
	mapTypeId: google.maps.MapTypeId.SATELLITE,
	disableDefaultUI: true,
	panControl: false,
	zoomControl: false,
	mapTypeControl: false,
	scaleControl: false,
	streetViewControl: false,
	overviewMapControl: false
    };
    var map = new google.maps.Map(document.getElementById(map_element_id), mapOptions);
    return map;
}

function addIcon(map, latitude, longitude, image_url, resource_name, resource_url, anchorX, anchorY, zIndex) {
    var myLatLng = new google.maps.LatLng(latitude, longitude);
    var image = new google.maps.MarkerImage(image_url,
	    new google.maps.Size(50, 49),
	    new google.maps.Point(0,0), // origin, if in sprite with many icons
	    new google.maps.Point(anchorX, anchorY)); // anchor
    var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          icon: image,
	  title: resource_name,
	  zIndex: zIndex
      });
    google.maps.event.addListener(marker, 'click', function() {
	window.location = resource_url;
    });
}

function addArrowIcon(map, latitude, longitude, image_url, resource_name, resource_url) {
    addIcon(map, latitude, longitude, image_url, resource_name, resource_url, 25, 49, 2);
}

function addResourceIcon(map, latitude, longitude, image_url, resource_name, resource_url) {
    addIcon(map, latitude, longitude, image_url, resource_name, resource_url, 25, 25, 1);
}
