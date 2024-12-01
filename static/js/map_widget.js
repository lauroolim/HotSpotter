var mapWidget = {
    map: null,
    marker: null,
    geocoder: null,
    
    init: function() {
        this.geocoder = new google.maps.Geocoder();
        
        var defaultLocation = new google.maps.LatLng(-10.2491, -48.3243);
        
        this.map = new google.maps.Map(document.getElementById('map_canvas'), {
            zoom: 13,
            center: defaultLocation,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        });
        
        this.marker = new google.maps.Marker({
            map: this.map,
            draggable: true,
            position: defaultLocation
        });
        
        this.setupEventListeners();
        this.setupAddressAutocomplete();
    },
    
    setupEventListeners: function() {
        var self = this;
        
        google.maps.event.addListener(this.marker, 'dragend', function() {
            self.updateCoordinates(self.marker.getPosition());
        });
        
        google.maps.event.addListener(this.map, 'click', function(event) {
            self.marker.setPosition(event.latLng);
            self.updateCoordinates(event.latLng);
        });
        
        document.getElementById('set_location').addEventListener('click', function() {
            self.updateCoordinates(self.marker.getPosition());
        });
    },
    
    setupAddressAutocomplete: function() {
        var self = this;
        var input = document.getElementById('address_input');
        var autocomplete = new google.maps.places.Autocomplete(input);
        
        autocomplete.addListener('place_changed', function() {
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                alert("No location found for the entered address.");
                return;
            }
            
            self.map.setCenter(place.geometry.location);
            self.marker.setPosition(place.geometry.location);
            self.updateCoordinates(place.geometry.location);
        });
    },
    
    updateCoordinates: function(location) {
        var coordinateInput = document.querySelector('.map-coordinate-input');
        coordinateInput.value = location.lat() + "," + location.lng();
        
        this.showNotification("Local definido com sucesso");
    },
    
    showNotification: function(message) {
        var notification = document.createElement('div');
        notification.className = 'alert alert-success';
        notification.style.position = 'fixed';
        notification.style.top = '20px';
        notification.style.right = '20px';
        notification.style.zIndex = '1000';
        notification.innerHTML = message;
        
        document.body.appendChild(notification);
        
        setTimeout(function() {
            notification.remove();
        }, 3000);
    }
};

document.addEventListener('DOMContentLoaded', function() {
    mapWidget.init();
});