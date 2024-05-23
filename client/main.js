import { addCoordinate } from "./http.js";

let map;
let coordinate = [];
let markers = [];
let paths = [];

map = L.map("map").setView([-7.873214892001908, 112.5200708249811], 20);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

var popup = L.popup();

const onMapClick = async (e) => {
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
    await addCoordinate(coordinate);
  }
};

map.on("click", onMapClick);
