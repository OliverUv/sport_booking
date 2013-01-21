function initializeMap(data) {
    var zoom_level = 15;
    if (data.hasOwnProperty('zoom_level'))
	zoom_level = data.zoom_level;
    if (is_mobile())
	zoom_level = 15;
    var scrollwheel = true;
    if (data.hasOwnProperty('scrollwheel'))
	scrollwheel = data.scrollwheel;
    var mapOptions = {
	center: new google.maps.LatLng(data.latitude, data.longitude),
	zoom: zoom_level,
	scrollwheel: scrollwheel,
	mapTypeId: google.maps.MapTypeId.SATELLITE,
	disableDefaultUI: true,
	panControl: false,
	zoomControl: false,
	mapTypeControl: false,
	scaleControl: false,
	streetViewControl: false,
	overviewMapControl: false
    };
    var map = new google.maps.Map(document.getElementById(data.element_id), mapOptions);
    return map;
}

function addSun(map, image_url) {
    var myLatLng = new google.maps.LatLng(27.064018, 8.102417);
    var image = new google.maps.MarkerImage(image_url,
	    new google.maps.Size(230, 240),
	    new google.maps.Point(0,0),
	    new google.maps.Point(115, 120));
    var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          icon: image,
	  title: "RUN",
	  zIndex: 1
      });
    google.maps.event.addListener(marker, 'click', function() {
	window.location = "http://youtu.be/Z-3z3DNUGiE";
    });
}

function addIcon(map, latitude, longitude, image_url, resource_name, resource_url, anchorX, anchorY, zIndex) {
    var myLatLng = new google.maps.LatLng(latitude, longitude);
    var image = new google.maps.MarkerImage(image_url,
	    new google.maps.Size(50, 50),
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
    return marker;
}

function addArrowIcon(map, latitude, longitude, image_url, resource_name, resource_url) {
    return addIcon(map, latitude, longitude, image_url, resource_name, resource_url, 25, 50, 2);
}

function addResourceIcon(map, latitude, longitude, image_url, resource_name, resource_url) {
    return addIcon(map, latitude, longitude, image_url, resource_name, resource_url, 25, 25, 1);
}

function zoomToBounds(map, bounds, max_zoom) {
	map.fitBounds(bounds);
	zoomChangeBoundsListener = google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
	    if (this.getZoom() > max_zoom){
		this.setZoom(max_zoom);
	    }
	});
	setTimeout(function(){google.maps.event.removeListener(zoomChangeBoundsListener)}, 2000);
}
