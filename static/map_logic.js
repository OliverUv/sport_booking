function initializeMap(data) {
    var zoom_level = 15;
    if (data.hasOwnProperty('zoom_level'))
	zoom_level = data.zoom_level;
    if (is_mobile())
	zoom_level = 15;
    var mapOptions = {
	center: new google.maps.LatLng(data.latitude, data.longitude),
	zoom: zoom_level,
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
