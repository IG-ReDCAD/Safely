"use strict";

function findNeigh() {
    let arrayneigh = new Array();
    $.get('/neighcoordinates.json', (res) => {
        arrayneigh[0] = res.api_key;
        for (let index in res.name) {
            if (index != 0) {
                arrayneigh[index] = {
                    "name": res.name[index],
                    "count_crime": res.count_crime[index]
                };
            }
        }
    });
    return arrayneigh;
}

function findCountCrime(json_neigh, neigh_name) {
    for (let i = 1; i < json_neigh.length; i++) {
        if (json_neigh[i].name == neigh_name) {
            return json_neigh[i].count_crime;
        }
    }
    return 0;
}

function checkNeigh(KEY, LAT, LNG) {
    let N_name = "";
    let url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${LAT},${LNG}&key=${KEY}`;
    return fetch(url)
        .then(response => response.json())
        .then(data => {
            let parts = data.results[0].address_components;
            parts.forEach(part => {
                if (part.types.includes("neighborhood")) {
                    //we found "neighborhood" inside the data.results[0].address_components[x].types array
                    N_name = part.long_name;
                }
            });
            return N_name;
        })
        .catch(err => console.warn(err.message));
}

let list_neighborhood=[];

async function calcultateScore(routes) {
    let json_neigh = findNeigh();
    let score_list = [];
    let numbercoordinates = 0;
    let score = 0;

    for (let index in routes) {
        let score = 0;
        const list_x = [];
        const list_y = [];
        let numbercoordinates = 0;
        let list_route_neigh = [];
        let key = json_neigh[0];
        for (let j in routes[index].legs[0].steps) {
            //for(let k in routes[index].legs[0].steps[j].lat_lngs){
            let latc, lngc;
            if (j !== (routes[index].legs[0].steps.length - 1)) {
                latc = routes[index].legs[0].steps[j].start_point.lat();
                lngc = routes[index].legs[0].steps[j].start_point.lng();
            } else {
                latc = routes[index].legs[0].steps[j].end_point.lat();
                lngc = routes[index].legs[0].steps[j].end_point.lng();
            }
            numbercoordinates += 1;
            // check the neighborhood from the coordinates
            list_x.push(latc);
            list_y.push(lngc);
            let neigh_name = await checkNeigh(key, latc, lngc);
            if (neigh_name != null) {
                //find the count_crime for the name of the neighborhood
                let count_crime = findCountCrime(json_neigh, neigh_name);
                list_route_neigh.push(neigh_name);
                score = score + count_crime;
                //} 
            }
        }
        //check the numberof crimes total to get the pcg or the number of coordinates
        score = score / numbercoordinates;
        list_neighborhood.push(list_route_neigh);
        //list_score.push({"route":routes[0],"score":score,"x":[,,],"y":[,,]})
        score_list.push({
            "route": routes[index],
            "score": score,
            "x": list_x,
            "y": list_y
        });
    }
    return score_list;
}

let best_list_neigh = [];

function calculateminScore(scores) {
    let min_score = scores[0].score;
    let min_index = 0;
    for (let index = 1; index < scores.length; index++) {
        if (min_score > scores[index].score) {
            min_score = scores[index].score;
            min_index = index;
        }
    }
    best_list_neigh = list_neighborhood[min_index];
    return min_score;
}

function sort_score(scores) {
    const list_score = new Array();
    for (let i = 0; i < scores.length; i++) {
        list_score[i] = scores[i].score;
    }

    let sorted_list = list_score.sort((a, b) => a - b);
    return sorted_list;
}

var map;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        mapTypeControl: false,
        center: {
            lat: 37.773972,
            lng: -122.431297
        },
        zoom: 13
    });
    new AutocompleteDirectionsHandler(map);
}


function AutocompleteDirectionsHandler(map) {
    this.map = map;
    this.originPlaceId = null;
    this.destinationPlaceId = null;
    this.travelMode = 'WALKING';
    this.provideRouteAlternatives = true;
    this.directionsService = new google.maps.DirectionsService;


    var originInput = document.getElementById('origin-input');
    var destinationInput = document.getElementById('destination-input');
    var modeSelector = document.getElementById('mode-selector');

    var originAutocomplete = new google.maps.places.Autocomplete(originInput);
    // Specify just the place data fields that you need.
    originAutocomplete.setFields(['place_id']);

    var destinationAutocomplete =
        new google.maps.places.Autocomplete(destinationInput);
    // Specify just the place data fields that you need.
    destinationAutocomplete.setFields(['place_id']);

    this.setupClickListener('changemode-walking', 'WALKING');
    // this.setupClickListener('changemode-transit', 'TRANSIT');
    this.setupClickListener('changemode-driving', 'DRIVING');

    this.setupPlaceChangedListener(originAutocomplete, 'ORIG');
    this.setupPlaceChangedListener(destinationAutocomplete, 'DEST');

    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(originInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(
        destinationInput);
    this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(modeSelector);
}

// Sets a listener on a radio button to change the filter type on Places
// Autocomplete.
AutocompleteDirectionsHandler.prototype.setupClickListener = function(
    id, mode) {
    var radioButton = document.getElementById(id);
    var me = this;

    radioButton.addEventListener('click', function() {
        me.travelMode = mode;
        me.route();
    });
};

AutocompleteDirectionsHandler.prototype.setupPlaceChangedListener = function(
    autocomplete, mode) {
    var me = this;
    autocomplete.bindTo('bounds', this.map);

    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        if (!place.place_id) {
            window.alert('Please select an option from the dropdown list.');
            return;
        }
        if (mode === 'ORIG') {
            me.originPlaceId = place.place_id;
        } else {
            me.destinationPlaceId = place.place_id;
        }
        me.route();
    });
};

let min_score;
let list_directionRender = [];

AutocompleteDirectionsHandler.prototype.route = function() {
    if (!this.originPlaceId || !this.destinationPlaceId) {
        return;
    }
    var me = this;

    this.directionsService.route({
            origin: {
                'placeId': this.originPlaceId
            },
            destination: {
                'placeId': this.destinationPlaceId
            },
            travelMode: this.travelMode,
            provideRouteAlternatives: this.provideRouteAlternatives
        },
        async function(response, status) {
            if (status === 'OK') {
                //calculate the score of each route
                let scores = await calcultateScore(response.routes);
                console.log("scores", scores);

                //calculate min of scores
                let sorted_scores = sort_score(scores);
                min_score = calculateminScore(scores);
                console.log("min score", min_score)

                //show directions
                let list_colors = ['green', 'blue', 'red'];
                let list_div = ['first', 'second', 'third'];
                let color = 'red';

                for (let i = 0, len1 = sorted_scores.length; i < len1; i++) {
                    for (let j = 0, len2 = scores.length; j < len2; j++) {
                        if (sorted_scores[i] === scores[j].score) {
                            this.directionsRenderer = new google.maps.DirectionsRenderer({
                                map: this.map,
                                directions: response,
                                routeIndex: i,
                                polylineOptions: {
                                    strokeColor: list_colors[i]
                                }
                            });
                            this.directionsRenderer.setMap(map);
                            list_directionRender.push({
                                "direction": this.directionsRenderer,
                                "div": list_div[i],
                                "score": sorted_scores[i],
                                "x": scores[j].x,
                                "y": scores[j].y
                            });
                            document.getElementById(list_div[i]).style.display = "block";
                        }
                    }

                }
                $('addRoute').css('visibility', 'visible');

            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });
};

//  add a route button
$("#addRoute").on("click", (evt) => {
    evt.preventDefault();

    const formInputs = {
        'start_address': $('#origin-input').val(),
        'end_address': $('#destination-input').val(),
        'name': $('#name-route').val(),
        'score': min_score,
        'list_neigh': JSON.stringify({
            "neigh": best_list_neigh
        })
    };

    $.post('/addRoute', formInputs, (res) => {
        alert(res);
    });
});

//  refresh button
$("#refresh").on("click", (evt) => {
    evt.preventDefault();
    window.location.reload();
});

// select a route from the three routes

function notify_user_high_crime_route(score) {
    if (score > 7000) {
        const formInputs = {
            'start_address': $('#origin-input').val(),
            'end_address': $('#destination-input').val(),
            'score': score
        };
        $.post('/sendm', formInputs, (res) => {
            alert(res);
        });
    }
}

let selected_index_route = 0;
$("#firstb").on("click", (evt) => {
    evt.preventDefault();
    let selected_score = 0;
    for (let x of list_directionRender) {
        if (x.div != "first") {
            x.direction.setMap(null);
        } else {
            selected_score = x.score;
            selected_index_route = 1;
        }
    }
    notify_user_high_crime_route(selected_score);
});

$("#secondb").on("click", (evt) => {
    evt.preventDefault();
    let selected_score = 0;
    for (let x of list_directionRender) {
        if (x.div != "second") {
            x.direction.setMap(null);
        } else {
            selected_score = x.score;
            selected_index_route = 2;
        }
    }
    notify_user_high_crime_route(selected_score);
});

$("#thirdb").on("click", (evt) => {
    evt.preventDefault();
    let selected_score = 0;
    for (let x of list_directionRender) {
        if (x.div != "third") {
            x.direction.setMap(null);
        } else {
            selected_score = x.score;
            selected_index_route = 3;
        }
    }
    notify_user_high_crime_route(selected_score);
});

// a share button: share the directions on the phone
$("#share").on("click", (evt) => {
    evt.preventDefault();
    const index = selected_index_route - 1;

    let waypoints = '';
    const link = 'https://www.google.com/maps/dir/?api=1'
    const xy = list_directionRender[index]
    for (let i = 0; i < xy.x.length; i++) {
        if (i != 0) {
            waypoints += '|';
        }
        waypoints += xy.x[i] + ',' + xy.y[i];
    }

    const formInputs = {
        'start_address': $('#origin-input').val(),
        'end_address': $('#destination-input').val(),
        'travelMode': $('#mode-selector input[name="type"][checked]').val(),
        'waypoints': waypoints,
        'link': link
    };
    $.post('/shareLink', formInputs, (res) => {
        alert("A message has been sent " + res);
    });
});