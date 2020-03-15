
const colors =  {'0':'#e5f5e0', '1':'#f7fcb9', '2':'#ffeda0','3':'#feb24c','4':'#fdae6b','5':'#fc9272','6':'#f03b20','7':'#e6550d', '8':'#de2d26'};
const category= ['2', '1', '2', '3', '5', '4', '1', '5', '4', '3', '3', '3', '3', '3', '4', '5', '5', '4', '8', '8', '7', '4', '4', '3', '4', '4', '3', '4', '3', '4', '4', '8', '4', '4', '0', '3', '5', '4', '5', '4', '4', '3', '3', '3', '3', '3', '2', '2', '2', '6', '3', '4', '8', '5', '4', '3', '3', '3', '3', '3', '3', '3', '1', '3', '3', '3', '3', '1', '1', '1', '3', '3', '1', '3', '4', '2', '5', '4', '3', '4', '3', '3', '5', '4', '3', '5', '4', '4', '3', '4', '5', '3', '3', '3', '3', '3', '5', '4', '6', '5', '5', '5', '4', '5', '4', '5', '5', '6', '4', '3', '2', '3', '3', '3', '3', '2', '1'];
function initMap() {

        // Initialize some map with center at Bucaramanga
        let map = new google.maps.Map(document.getElementById('map'), {
            center: {
                lat: 37.7749, 
                lng: -122.4194
            },
            zoom: 12,
            mapTypeId: 'roadmap'
        });

    let coordinates = []
    let BucaramangaDelimiters;
  $.post('/getNeigh', (res) => {
     for (let eachneigh of res){
        coordinates.push(Object.values(eachneigh));
     }
     let index=0;
     for(let eachCoorCat of coordinates){
        BucaramangaDelimiters = eachCoorCat[0].coordinates;

        let BucaramangaPolygon = new google.maps.Polygon({
            paths: BucaramangaDelimiters,
            strokeColor: colors[category[index]],
            strokeOpacity: 0.8,
            strokeWeight: 3,
            fillColor: colors[category[index]],
            fillOpacity: 0.35
        });
        index+=1

        // Draw the polygon on the desired map instance
        BucaramangaPolygon.setMap(map);
     }  
  });
}

// Results:
// Seacliff 144 2
// Lake Street 82 1
// Presidio National Park 162 2
// Presidio Terrace 201 3
// Inner Richmond 3062 5
// Sutro Heights 1053 4
// Lincoln Park / Ft. Miley 88 1
// Outer Richmond 3418 5
// Golden Gate Park 1802 4
// Presidio Heights 372 3
// Laurel Heights / Jordan Park 673 3
// Lone Mountain 796 3
// Anza Vista 674 3
// Cow Hollow 547 3
// Union Street 1439 4
// Nob Hill 2058 5
// Marina 3444 5
// Telegraph Hill 999 4
// Downtown / Union Square 10553 8
// Tenderloin 11032 8
// Civic Center 7384 7
// Hayes Valley 1682 4
// Alamo Square 1297 4
// Panhandle 749 3
// Haight Ashbury 1824 4
// Lower Haight 1652 4
// Mint Hill 361 3
// Duboce Triangle 1864 4
// Cole Valley 260 3
// Rincon Hill 1199 4
// South Beach 1329 4
// South of Market 19491 8
// Showplace Square 1446 4
// Mission Bay 1637 4
// Yerba Buena Island 0 0
// Treasure Island 554 3
// Mission Dolores 3070 5
// Castro 1755 4
// Outer Sunset 3099 5
// Parkside 1317 4
// Stonestown 1405 4
// Parkmerced 845 3
// Lakeshore 483 3
// Golden Gate Heights 782 3
// Forest Hill 191 3
// West Portal 384 3
// Clarendon Heights 156 2
// Midtown Terrace 97 2
// Laguna Honda 182 2
// Lower Nob Hill 4580 6
// Upper Market 913 3
// Dolores Heights 1104 4
// Mission 15836 8
// Potrero Hill 3578 5
// Dogpatch 1064 4
// Central Waterfront 777 3
// Diamond Heights 417 3
// Crocker Amazon 575 3
// Fairmount 360 3
// Peralta Heights 337 3
// Holly Park 556 3
// Merced Manor 321 3
// Balboa Terrace 67 1
// Ingleside 953 3
// Merced Heights 566 3
// Outer Mission 597 3
// Ingleside Terraces 400 3
// Mt. Davidson Manor 76 1
// Monterey Heights 74 1
// Westwood Highlands 29 1
// Westwood Park 325 3
// Miraloma Park 318 3
// McLaren Park 92 1
// Sunnydale 773 3
// Visitacion Valley 1241 4
// India Basin 145 2
// Northern Waterfront 2141 5
// Hunters Point 1195 4
// Candlestick Point SRA 207 3
// Cayuga 1226 4
// Oceanview 600 3
// Apparel City 677 3
// Bernal Heights 1975 5
// Noe Valley 1132 4
// Produce Market 633 3
// Bayview 3678 5
// Silver Terrace 1606 4
// Bret Harte 1124 4
// Little Hollywood 210 3
// Excelsior 1244 4
// Portola 2099 5
// University Mound 281 3
// St. Marys Park 246 3
// Mission Terrace 948 3
// Sunnyside 504 3
// Glen Park 464 3
// Western Addition 3187 5
// Aquatic Park / Ft. Mason 1281 4
// Fishermans Wharf 4898 6
// Cathedral Hill 2353 5
// Japantown 2312 5
// Pacific Heights 2559 5
// Lower Pacific Heights 1858 4
// Chinatown 2269 5
// Polk Gulch 1335 4
// North Beach 2859 5
// Russian Hill 2916 5
// Financial District 4307 6
// Inner Sunset 1375 4
// Parnassus Heights 203 3
// Forest Knolls 102 2
// Buena Vista 775 3
// Corona Heights 271 3
// Ashbury Heights 204 3
// Eureka Valley 661 3
// St. Francis Wood 152 2
// Sherwood Forest 90 1
