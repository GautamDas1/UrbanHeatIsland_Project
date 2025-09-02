import React, { useState, useEffect, useRef } from "react";
import MapView from "./MapView";
import Metrics from "./Metrics";
import Graph from "./Graph";
import axios from "../api/axios";

const UHIApp = ({ cities }) => {
  const [selectedCity, setSelectedCity] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  const mapRef = useRef();

  // Handle city selection from dropdown
  const handleCityChange = async (city) => {
    setSelectedCity(city);
    setLoading(true);

    try {
      const res = await axios.get("/predict", {
        params: { lat: city.lat, lon: city.lon, city: city.name },
      });

      const heatRes = await axios.get("/heatmap");

      const heatmapPoints = heatRes.data.heatmap.map((h) => [
        h.lat,
        h.lon,
        h.intensity,
      ]);

      mapRef.current?.displayHeatmap(heatmapPoints, [res.data]);
    } catch (err) {
      console.error("Error fetching backend data:", err);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Dropdown for cities */}
      <div>
        <select
          className="border p-2 rounded"
          onChange={(e) => {
            const city = cities.find((c) => c.name === e.target.value);
            if (city) handleCityChange(city);
          }}
        >
          <option value="">Select a city</option>
          {cities.map((c) => (
            <option key={c.name} value={c.name}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {/* Metrics and Graph */}
      <div className="flex flex-col md:flex-row gap-4">
        <Metrics metrics={metrics} loading={loading} />
        <Graph chartData={chartData} loading={loading} />
      </div>

      {/* Map */}
      <MapView
        ref={mapRef}
        selectedCity={selectedCity}
        setMetrics={setMetrics}
        setChartData={setChartData}
        setLoading={setLoading}
      />
    </div>
  );
};

export default UHIApp;
