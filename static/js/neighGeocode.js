"use strict";

let n = 0;
$('#neighborhood').on('click', () => {
  //create a dictionary in which we return the result of the search.
  let arrayneigh = new Array();
  $.get(`/neighcoordinates.json`, (res) => {
    const KEY = res.api_key;
    for (let index in res.name) {
      const LAT = res.latitude[index];
      const LNG = res.longitude[index];
      const N_id = res.id[index];
      let N_name = "";
      let url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${LAT},${LNG}&key=${KEY}`;
      fetch(url)
        .then(response => response.json())
        .then(data => {
          let parts = data.results[0].address_components;
          document.body.insertAdjacentHTML(
            "beforeend", `<p>Formatted: ${data.results[0].formatted_address}</p>`
          );
          parts.forEach(part => {
            if (part.types.includes("country")) {
              //we found "country" inside the data.results[0].address_components[x].types array
              document.body.insertAdjacentHTML(
                "beforeend", `<p>COUNTRY: ${part.long_name}</p>`
              );
            }
            if (part.types.includes("neighborhood")) {
              document.body.insertAdjacentHTML(
                "beforeend", `<p>neighborhood: ${part.long_name}</p>`
              );
              N_name = part.long_name;
              arrayneigh[index] = {
                "name": N_name,
                "latitude": LAT,
                "longitude": LNG,
                "number": index
              }
              $.post("/neighc", {
                "name": N_name,
                "latitude": LAT,
                "longitude": LNG,
                "number": index,
                "id": N_id
              }, res);
            }
            if (part.types.includes("administrative_area_level_1")) {
              document.body.insertAdjacentHTML(
                "beforeend", `<p>PROVINCE: ${part.long_name}</p>`
              );
            }
            if (part.types.includes("administrative_area_level_3")) {
              document.body.insertAdjacentHTML(
                "beforeend", `<p>LEVEL 3: ${part.long_name}</p>`
              );
            }
          });
        })
        .catch(err => console.warn(err.message));
    }
    console.log("done", arrayneigh);
  });
});