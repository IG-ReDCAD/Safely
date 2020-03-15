"use strict"

// We chose to attach all our event listeners in this function since this is
// where the `map` object is in-scope.
//
// There are other ways to do this. Another way to make sure `map` is in-scope
// is to define functions outside of `initMap` that take in a Google Map
// object as an argument.
function initMap() {
  let map = new google.maps.Map($('#map')[0], {
    center: {
      lat: 37.601773,
      lng: -122.202870
    },
    zoom: 11,
  });


  // Apply custom styles to a map. In this example, we just make the
  // water pink.
  $('#custom-style').on('click', () => {
    const customStyledMap = new google.maps.StyledMapType(
      [
        {
          featureType: 'water',
          elementType: 'geometry.fill',
          stylers: [{ color: '#ffd1e4' }]
        }
      ]
    );

    map.mapTypes.set('map_style', customStyledMap);
    map.setMapTypeId('map_style');
  });


  // Ask user to enter a location. Geocode the location to get its coordinates
  // and drop a marker onto the map. 
  $('#geocode-address').on('click', () => {
    const userAddress = prompt('Enter a location');

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userAddress }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;

        // Create a marker
        const userLocationMarker = new google.maps.Marker({
          position: userLocation,
          map: map
        });

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(18);
      } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
    });
  });


  //drop a maker onto the map for each neighborhood.
  $('#neighborhood-address').on('click', () => {
    //const userAddress = prompt('Enter a location');

    $.get(`/neighcoordinates.json`, (res) => {
        const geocoder = new google.maps.Geocoder();
        //geocoder.geocode({ address: userAddress }, (results, status) => {


        let arrayCoordinates = new Array();  
        let index = 0;
        for(let eachneigh of res.name){
          console.log(eachneigh);
          if(eachneigh!="nan" && eachneigh!="NaN" && eachneigh!="null"){
            let neighborhood_name= eachneigh + " San Francisco, CA, USA";

            //look for the place autocomplite
            let request = {
              query: neighborhood_name,
              fields: ['name', 'geometry'],
            };

            let service = new google.maps.places.PlacesService(map);
            if (service!="null"){
              service.findPlaceFromQuery(request, function(results, status) {
                console.log(results);
                let latitude=results[0].geometry.location.lat();
                console.log(eachneigh + latitude);
                let longitude=results[0].geometry.location.lng();
                arrayCoordinates[index]={"name":eachneigh,"latitude":latitude,"longitude":longitude};
                index++;
              });
            }
            

              // viewport contains the recommended viewport for displaying the returned result, 
              //specified as two latitude,longitude values defining the southwest and northeast corner of the viewport bounding box.
              // Generally the viewport is used to frame a result when displaying it to a user.
              // console.log(results[0].geometry.viewport.Ya)
              // console.log(results[0].geometry.viewport.Ta)
            
          }


        // geocoder.geocode(neighborhood_name, (results, status) => {
        //   console.log("inside")
        //   console.log(status);
          
        //   if (status === 'OK') {
        //     // Get the coordinates of the user's location
        //     const userLocation = results[0].geometry.location;
        //     console.log(results[0]);

        //     // Create a marker
        //     const userLocationMarker = new google.maps.Marker({
        //       position: userLocation,
        //       map: map
        //     });

        //     // Zoom in on the geolocated location
        //     map.setCenter(userLocation);
        //     map.setZoom(18);
        //   } else {
        //     alert(`Geocode was unsuccessful for the following reason: ${status}`);
        //   }
        // });
        } 
        let neighJson = {dic_neigh: arrayCoordinates};
        console.log(neighJson);
        let asJSON = JSON.stringify(neighJson);
        

    });  
  });


  // Draw a line on the map from Hackbright to Powell Street Station to
  // Montgomery Station
  $('#draw-polyline').on('click', () => {
    const polyline = new google.maps.Polyline({
      path: [
        {
          lat: 37.7887459,  // Hackbright
          lng: -122.4115852
        },
        {
          lat: 37.7844605,  // Powell Street Station
          lng: -122.4079702
        },
        {
          lat: 37.7894094,  // Montgomery Station
          lng: -122.4013037
        },
      ],
      geodesic: true,
      strokeColor: '#ff0000',
      strokeOpacity: 1.0,
      strokeWeight: 5
    });

    polyline.setMap(map);
  });


  // Display walking directions from Hackbright to Powell Street Station
  // on the map
  $('#display-directions').on('click', () => {
    const directionsService = new google.maps.DirectionsService();

    // The DirectionsRenderer object is in charge of drawing directions
    // on maps
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    const hbToPowellRoute = {
      origin: {
        lat: 37.7887459,
        lng: -122.4115852
      },
      destination: {
        lat: 37.7844605,
        lng: -122.4079702
      },
      travelMode: 'WALKING'
    };

    directionsService.route(hbToPowellRoute, (response, status) => {
      if (status === 'OK') {
        directionsRenderer.setDirections(response);
      } else {
        alert(`Directions request unsuccessful due to: ${status}`);
      }
    });

  });


  // This is NOT a Google Maps API-related thing. This actually uses a Web
  // API called the Geolocation API. Most browsers have geolocation built-in!
  //
  // For reference, here's documenation on the Geolocation API:
  //     https://developer.mozilla.org/en-US/docs/Web/API/Geolocation
  $('#geolocate-me').on('click', () => {
    // If the browser has geolocation-capabilities, it'll be stored on a global
    // object called `navigator`. (Most modern browsers will have this.)
    //
    // If `navigator.geolocation` is `undefined`, then your user has a pretty
    // old browser :(
    if (navigator.geolocation) {
      // `navigator.geolocation.getCurrentPosition` takes in two args:
      //
      // - A function that is called when we successfully get the
      //   user's location
      //
      // - A function that's called when we can't get the user's location
      //   (probably because they didn't allow your page to access it)
      navigator.geolocation.getCurrentPosition(
        // The success function:
        (currPosition) => {
          alert('Going to your location now!');

          map.setCenter({
            lat: currPosition.coords.latitude,
            lng: currPosition.coords.longitude
          });
          map.setZoom(18);
        },
        // The unsuccessful function:
        () => {
          alert('Unable to get your location :(');
        }
      );
    } else {
      alert(`Your browser doesn't support geolocation`);
    }
  });
}
