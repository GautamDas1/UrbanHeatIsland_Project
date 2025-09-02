import React, { useEffect, useRef, useImperativeHandle, forwardRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-draw";
import "leaflet-draw/dist/leaflet.draw.css";
import "leaflet.heat";
import axios from "../api/axios";

// Fix for default Leaflet marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
});

const MapView = forwardRef(({ selectedCity, setMetrics, setChartData, setLoading }, ref) => {
  const mapRef = useRef(null);
  const drawnItemsRef = useRef(null);
  const heatLayerRef = useRef(null);

  useImperativeHandle(ref, () => ({
    displayHeatmap: (heatmapPoints, predictions) => {
      if (!mapRef.current) return;

      if (heatLayerRef.current) {
        mapRef.current.removeLayer(heatLayerRef.current);
      }

      if (heatmapPoints?.length > 0) {
        heatLayerRef.current = L.heatLayer(heatmapPoints, {
          radius: 25,
          blur: 20,
          maxZoom: 17,
          gradient: { 0.0: "blue", 0.4: "lime", 0.6: "yellow", 0.8: "orange", 1.0: "red" },
        }).addTo(mapRef.current);
      }

      if (predictions?.length > 0) {
        const firstPrediction = predictions[0];
        setMetrics({
          city: firstPrediction.city,
          level: firstPrediction.level,
          avg_temp: firstPrediction.avg_temp.toFixed(2),
          mitigated_temp: firstPrediction.mitigated_temp.toFixed(2),
        });
        setChartData([
          { name: "Original", value: firstPrediction.avg_temp },
          { name: "Mitigated", value: firstPrediction.mitigated_temp },
        ]);
      } else {
        setMetrics({
          city: "Custom Location",
          level: "High",
          avg_temp: 0,
          mitigated_temp: 0,
        });
        setChartData([]);
      }

      setLoading(false);
    },
  }));

  useEffect(() => {
    if (!mapRef.current) {
      mapRef.current = L.map("map", { center: [20.5937, 78.9629], zoom: 5 });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
      }).addTo(mapRef.current);

      drawnItemsRef.current = new L.FeatureGroup();
      mapRef.current.addLayer(drawnItemsRef.current);

      const drawControl = new L.Control.Draw({
        draw: { polygon: true, rectangle: true, circle: false, polyline: false, marker: true, circlemarker: false },
        edit: { featureGroup: drawnItemsRef.current },
      });
      mapRef.current.addControl(drawControl);

      mapRef.current.on(L.Draw.Event.CREATED, async (e) => {
        drawnItemsRef.current.clearLayers();
        drawnItemsRef.current.addLayer(e.layer);

        let center = e.layer.getLatLng ? e.layer.getLatLng() : e.layer.getBounds().getCenter();
        if (center) {
          setLoading(true);

          try {
            // Fetch real satellite-based metrics
            const metricsRes = await axios.get("/predict", {
              params: { lat: center.lat, lon: center.lng, city: "Custom Location" },
            });

            // Fetch heatmap points
            const heatmapRes = await axios.get("/heatmap");
            const heatmapPoints = heatmapRes.data.heatmap.map((h) => [h.lat, h.lon, h.intensity]);

            ref.current?.displayHeatmap(heatmapPoints, [metricsRes.data]);
          } catch (err) {
            console.error("Error fetching backend data:", err);
            // Fallback dummy metrics
            setMetrics({ city: "Custom Location", level: "High", avg_temp: 0, mitigated_temp: 0 });
            setChartData([]);
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

  useEffect(() => {
    if (selectedCity && mapRef.current) {
      if (selectedCity.lat && selectedCity.lon) {
        mapRef.current.flyTo([selectedCity.lat, selectedCity.lon], 12);
        drawnItemsRef.current.clearLayers();
        L.marker([selectedCity.lat, selectedCity.lon]).addTo(drawnItemsRef.current);
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
