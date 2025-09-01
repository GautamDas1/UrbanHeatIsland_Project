import React, { useEffect, useRef, useImperativeHandle, forwardRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";
import "leaflet.heat";

// Fix for default Leaflet marker icons not showing
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const MapView = forwardRef(({ selectedCity, setMetrics, setChartData, setLoading }, ref) => {
  const mapRef = useRef(null);
  const drawnItemsRef = useRef(null);
  const heatLayerRef = useRef(null);

  // Expose displayHeatmap for manual triggering
  useImperativeHandle(ref, () => ({
    displayHeatmap: (heatmapPoints, predictions) => {
      if (!mapRef.current) return;

      if (heatLayerRef.current) {
        mapRef.current.removeLayer(heatLayerRef.current);
      }

      if (heatmapPoints?.length > 0) {
        heatLayerRef.current = L.heatLayer(heatmapPoints, {
          radius: 25,
          blur: 15,
          maxZoom: 17,
          gradient: { 0.0: 'blue', 0.5: 'lime', 1.0: 'red' }
        }).addTo(mapRef.current);
      }

      if (predictions?.length > 0) {
        const firstPrediction = predictions[0];
        setMetrics({
          level: firstPrediction.uhi_level,
          avg: firstPrediction.average_temperature_celsius,
        });
        setChartData([
          { name: "Original", value: firstPrediction.average_temperature_celsius },
          { name: "Mitigated", value: firstPrediction.mitigated_temperature_celsius },
        ]);
      } else {
        setMetrics(null);
        setChartData([]);
      }

      setLoading(false);
    }
  }));

  // Initialize map
  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map", {
        center: [20.5937, 78.9629],
        zoom: 5,
      });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      }).addTo(mapRef.current);

      drawnItemsRef.current = new L.FeatureGroup();
      mapRef.current.addLayer(drawnItemsRef.current);

      const drawControl = new L.Control.Draw({
        draw: {
          polygon: true,
          rectangle: true,
          circle: false,
          polyline: false,
          marker: true,
          circlemarker: false,
        },
        edit: { featureGroup: drawnItemsRef.current },
      });
      mapRef.current.addControl(drawControl);

      // On shape drawn
      mapRef.current.on(L.Draw.Event.CREATED, async (e) => {
        drawnItemsRef.current.clearLayers();
        drawnItemsRef.current.addLayer(e.layer);

        let center;
        if (e.layer.getLatLng) {
          center = e.layer.getLatLng();
        } else {
          center = e.layer.getBounds().getCenter();
        }

        if (center) {
          setLoading(true);
          try {
            const res = await fetch("http://127.0.0.1:5000/api/map-data", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ lat: center.lat, lon: center.lng })
            });
            const data = await res.json();

            if (data.heatmap && data.predictions) {
              ref.current?.displayHeatmap(data.heatmap, data.predictions);
            } else {
              setMetrics(null);
              setChartData([]);
              setLoading(false);
            }
          } catch (err) {
            console.error("Error fetching map data:", err);
            setLoading(false);
          }
        }
      });
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  // Fly to city when selected
  useEffect(() => {
    if (selectedCity && mapRef.current) {
      const cityData = selectedCity.value || selectedCity;
      if (cityData.lat && cityData.lon) {
        mapRef.current.flyTo([cityData.lat, cityData.lon], 12);
        drawnItemsRef.current.clearLayers();
        L.marker([cityData.lat, cityData.lon]).addTo(drawnItemsRef.current);
      }
    }
  }, [selectedCity]);

  return (
    <div
      id="map"
      style={{ height: "500px", width: "100%" }}
      className="rounded-lg shadow-lg border border-gray-300"
    />
  );
});

export default MapView;
