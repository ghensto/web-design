
/* global google, pname, paddress */

var map;
var request;
var umn;
var service;
var geocoder = new google.maps.Geocoder();
var fplace = [];
var markers = [];
var i;
var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
var org;


function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9727, lng: -93.23540000000003},
        zoom: 14
    });
    
    service = new google.maps.places.PlacesService(map);
    places();
    geolocate();
}

// ===================================== Displays Favorites places on the map ===================
function places(){
    var l = document.getElementsByClassName("pName").length;
    var n = document.getElementsByClassName("pName");
    var ad = document.getElementsByClassName("address");
    
    for (var j = 0; j < l; j++){
        fplace.push([n[j].textContent.trim().toString(), ad[j].textContent.trim().toString()]); 
    }
    geocodeAddress(geocoder, map);
}
function geocodeAddress(geocoder, resultsMap) {
    
    var name = [];
    var m = 0;
    var infoWindow = new google.maps.InfoWindow();
    for (var k = 0; k < fplace.length; k++) {
        var address = fplace[k][1];
        name[k] = fplace[k];
        geocoder.geocode({'address': address}, function (results, status) {
            if (status === 'OK') {
                resultsMap.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    //title: t,
                    map: resultsMap,
                    position: results[0].geometry.location,
                    icon: image
                    //animation: google.maps.Animation.BOUNCE
                });
                //marker.setAnimation();;
                var sub = "<b>" + name[m][0] + "</b> <br/>" + name[m][1];
                m++;
                google.maps.event.addListener(marker, 'click', (function(marker){
                    return function () {
                        infoWindow.setContent(sub);
                        infoWindow.open(map, marker);
                    };
                })(marker));
                markers.push(marker);
            } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }
}
//==========================================================================================

// ============================== Radar search of place near me =====================
function search() {
    if (org != null){
        map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9727, lng: -93.23540000000003},
        zoom: 14
    });
    }
    
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.length = 0;
    var rad = document.getElementById('rads').value;
    var near = document.getElementById('nearby').value;
    umn = new google.maps.LatLng(44.9727,-93.23540000000003);
    service.nearbySearch({
        location: umn,
        radius: parseInt(rad),
        type: [near]
    }, callback);
}


function callback(results, status) {
  if (status === google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      var place = results[i];
      createMarker(place);
    }
  }
}

function createMarker(place) {
	//var bounds = new google.maps.LatLngBounds();
    var infowindow = new google.maps.InfoWindow();
    var placeLoc = place.geometry.location;
    var marker = new google.maps.Marker({
        map: map,
        position: placeLoc
    });
	//bounds.extend(placeLoc);
    google.maps.event.addListener(marker, 'click', function () {
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
    markers.push(marker);
	//map.fitBounds(bounds);
}
// =====================================================================================

// ======================================== Gets Directions to a place =================

function directions() {
    var directionsService = new google.maps.DirectionsService;
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9727, lng: -93.23540000000003},
        mapTypeId: 'roadmap',
        zoom: 14
    });
    var directionsDisplay = new google.maps.DirectionsRenderer({
        panel: document.getElementById('right-panel')
    });
    document.getElementById('right-panel').innerHTML = '';
    directionsDisplay.setMap(map);
    dest = document.getElementById("destin").value;
    displayRoute(org, dest, directionsService, directionsDisplay);
    
}

function displayRoute(origin, destination, service, display) {
    var selectedMode = document.getElementById('dest').value;
    service.route({
        origin: new google.maps.LatLng(origin),
        destination: destination,
        travelMode: google.maps.TravelMode[selectedMode]
    }, function (response, status) {
        if (status === 'OK') {
            display.setDirections(response);
            computeTotalDistance(display.getDirections());
        } else {
            alert('Could not display directions due to: ' + status);
        }
    });
}

function computeTotalDistance(result) {
    var total = 0;
    var myroute = result.routes[0];
    for (var i = 0; i < myroute.legs.length; i++) {
        total += myroute.legs[i].distance.value;
    }
    total = total / 1000;
    //document.getElementById('total').innerHTML = total + ' km';
}

function geolocate() {
    infoWindow = new google.maps.InfoWindow;
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            map.setCenter(pos);
            org = pos;
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }
// ==========================================================================================

// =================================== Form ====================================================
function validate() {
    var p = document.getElementById('pname').value;
    var adl1 = document.getElementById('ad1').value;
    var adl2 = document.getElementById('ad2').value;
    var ap = /^[0-9a-zA-Z\d\s]+$/;
    
    if ((p.search(ap) !== 0) ) {
        alert("Place Name must be alphanumeric");
        return false;
    }
    else if ((adl1.search(ap) !== 0)) {
        alert("Address line 1 must be alphanumeric");
        return false;
    }
    else if ((adl2.search(ap) !== 0)) {
        alert("Address line 2 must be alphanumeric");
        return false;
    }
    else {
        return true;
    }

}
// =============================================================================================
