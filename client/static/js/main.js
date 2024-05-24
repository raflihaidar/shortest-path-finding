import { addCoordinate } from "./http.js";

let map;
let coordinate = [];

map = L.map("map").setView([-7.873214892001908, 112.5200708249811], 20);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

var popup = L.popup();

const onMapClick = async (e) => {
  try {
    if (coordinate.length < 2) {
      popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);

      let marker = new L.Marker(e.latlng);

      marker.addTo(map);

      let payload = {
        lat: e.latlng.lat,
        lng: e.latlng.lng,
      };

      coordinate.push(payload);
    } else {
      let message = await addCoordinate(coordinate);
      console.log(message);
    }
  } catch (error) {
    console.log(error);
  }
};

map.on("click", onMapClick);
