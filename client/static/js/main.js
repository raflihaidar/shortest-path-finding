import { addCoordinate } from "./http.js";
import { locations } from "./locations.js";

let map;
let coordinate = [];
let markers = [];
let route = [];
let polylines = [];

map = L.map("map").setView([-7.871203275411919, 112.5268921078188], 14);

let showAllBtn = document.getElementById("show-all-nodes");
let drawBtn = document.getElementById("draw-graph");
let isShow = false;

const showAllNodes = () => {
  isShow = true;
  for (let i = 0; i < locations.length; i++) {
    let marker = new L.marker([locations[i][1], locations[i][2]])
      .bindPopup(locations[i][0])
      .addTo(map)
      .on("click", onMapClick);
    markers.push(marker);
  }
  drawBtn.style.display = "block";
};

const hideAllNodes = () => {
  isShow = false;
  drawBtn.style.display = "none";
  markers.forEach((marker) => {
    map.removeLayer(marker);
  });
  polylines.forEach((polyline) => {
    map.removeLayer(polyline);
  });
  polylines = [];
};

const drawGraph = () => {
  for (let i = 0; i < locations.length; i++) {
    if (i + 1 < locations.length) {
      let polyline = new L.polyline([
        [locations[i][1], locations[i][2]],
        [locations[i + 1][1], locations[i + 1][2]],
      ]).addTo(map);
      polylines.push(polyline);
    }
  }
};

showAllBtn.addEventListener("click", () => {
  if (isShow) {
    showAllBtn.textContent = "Show All Nodes";
    hideAllNodes();
  } else {
    showAllBtn.textContent = "Hide All Nodes";
    showAllNodes();
  }
});

drawBtn.addEventListener("click", drawGraph);

const showModal = () => {
  document.getElementById("modal").style.display = "block";
};

const hideModal = () => {
  document.getElementById("modal").style.display = "none";
};

const onMapClick = async (e) => {
  try {
    if (coordinate.length < 2) {
      let marker = new L.circleMarker(e.latlng, { color: "#Ff0000" });
      marker.addTo(map);

      let payload = {
        lat: e.latlng.lat,
        lng: e.latlng.lng,
      };

      coordinate.push(payload);
    } else {
      showModal(); // Show modal while waiting for the route calculation
      route = await addCoordinate(coordinate);
      hideModal(); // Hide modal after route calculation is done

      let polyline = L.polyline(route, {
        color: "red",
        weight: 3,
        opacity: 1,
        smoothFactor: 1,
      });
      polyline.addTo(map);
      let myMovingMarker = L.Marker.movingMarker(route, 6000, {
        autostart: true,
      });

      map.addLayer(myMovingMarker);
      myMovingMarker.start();
    }
  } catch (error) {
    hideModal(); // Hide modal in case of an error
    console.log(error);
  }
};

let cityBounds = L.latLngBounds(
  L.latLng(-7.9325478493, 112.4523252469), // Koordinat barat daya
  L.latLng(-7.7592663752, 112.6113239877) // Koordinat timur laut
);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
  minZoom: 12,

  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

L.control.scale().addTo(map);

map.setMaxBounds(cityBounds);

for (let i = 0; i < locations.length; i++) {
  let marker = new L.marker([locations[i][1], locations[i][2]])
    .bindPopup(locations[i][0])
    .addTo(map)
    .on("click", onMapClick);

  markers.push(marker);
}

let popup = L.popup();

map.on("click", onMapClick);

const locationList = document.querySelectorAll(".location-item");

locationList.forEach((el, index) => {
  el.addEventListener("click", () => {
    markers[index].addTo(map);
    const lat = parseFloat(el.getAttribute("data-lat"));
    const lng = parseFloat(el.getAttribute("data-lng"));
    map.setView([lat, lng], 17);
    markers[index].openPopup();
  });
});

markers.forEach((marker) => {
  map.removeLayer(marker);
});
