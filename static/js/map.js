function initMap() {
  console.log('lat_a:', lat_a);
  console.log('long_a:', long_a);
  console.log('lat_b:', lat_b);
  console.log('long_b:', long_b);

  if (lat_a && long_a && lat_b && long_b) {
      var directionsService = new google.maps.DirectionsService();
      var directionsRenderer = new google.maps.DirectionsRenderer();
      var map = new google.maps.Map(document.getElementById('map-route'), {
          zoom: 7,
          center: { lat: parseFloat(lat_a), lng: parseFloat(long_a) }
      });
      directionsRenderer.setMap(map);

      var start = { lat: parseFloat(lat_a), lng: parseFloat(long_a) };
      var end = { lat: parseFloat(lat_b), lng: parseFloat(long_b) };

      directionsService.route(
          {
              origin: start,
              destination: end,
              travelMode: 'DRIVING',
          },
          function (response, status) {
              if (status === 'OK') {
                  directionsRenderer.setDirections(response);
              } else {
                  alert('Directions request failed due to ' + status);
              }
          }
      );
  } else {
      alert('Missing coordinates for map display.');
  }
}

// Initialize the map when the page loads
document.addEventListener('DOMContentLoaded', function () {
  initMap();
});