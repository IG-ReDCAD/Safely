"use strict";

function initMap() {
    const neighMap = new google.maps.Map(document.querySelector('#map'), {
        center: {
            lat: 37.7749,
            lng: -122.4194
        },
        zoom: 12
    });

    let locations = [];
    const markers = [];

    $.get('/coordinates.json', (res) => {
        let i = 0;
        for (const location of res) {
            let marker = new google.maps.Marker({
                position: location.coords,
                title: location.name,
                map: neighMap,
                icon: {
                    url: 'https://www.festivalclaca.cat/pics/b/37/370643_map-marker-png.png',
                    scaledSize: {
                        width: 30,
                        height: 30
                    }
                }
            });

            const markerInfo = (`<div id="iw-container">
                <div class="iw-title">${marker.title}</div>
                <div class="iw-content">
                <div class="iw-subTitle">History</div>
                <p>Date: ${location.date}</p>
                <p>Day: ${location.day}</p>
                <p>Time: ${location.time}</p>
                <p>Intersection: ${location.intersection}</p>
                <p>
                  Located at: <code>${marker.position.lat()}</code>,
                  <code>${marker.position.lng()}</code>
                </p>`);
            
            const infoWindow = new google.maps.InfoWindow({
                content: markerInfo,
                maxWidth: 400
            });
            marker.addListener('click', () => {
                if (marker.getAnimation() !== null) {
                    marker.setAnimation(null);
                } else {
                    marker.setAnimation(google.maps.Animation.BOUNCE);
                }
                infoWindow.open(neighMap, marker);
            });
            markers.push(marker);
        }
    });
}
