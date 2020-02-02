var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 39.1031, lng: -84.5120},
    zoom: 6
  });
}
