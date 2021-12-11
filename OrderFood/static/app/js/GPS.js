function initMap(){
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"),{
        zoom: 14,
        center: {lat: -33.05 , lng: -71.45 },
    });

    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    document.getElementById("mode").addEventListener("change", () => {
        calculateAndDisplayRoute(directionsService, directionsRenderer);
    });
}

function calculateAndDisplayRoute(directionsService, directionsRenderer){
    directionsService.route({
        origin: document.getElementById("from").value,
        destination: document.getElementById("to").value,
        travelMode: 'DRIVING'

    }, function(response, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(response);
  
  
        } else {
  
          window.alert('Directions request failed due to ' + status);
        }
      });
}