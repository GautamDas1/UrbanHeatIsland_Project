// src/components/UHIApp.jsx
import React, { useState, useRef } from "react";
import CitySearch from "./CitySearch";
import Metrics from "./Metrics";
import MapView from "./MapView";
import Graph from "./Graph";

const UHIApp = ({ cities }) => {
  const [selectedCity, setSelectedCity] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  const mapRef = useRef(null);

  const handleCityChange = (city) => {
    setSelectedCity(city);
    setLoading(true);

    // If the backend already returns metrics for this city, we use it
    if (city.avg_temp && city.mitigated_temp) {
      const cityMetrics = {
        city: city.value,
        avg_temp: city.avg_temp,
        mitigated_temp: city.mitigated_temp,
        level: city.level || "Medium",
      };
      setMetrics(cityMetrics);
      setChartData([
        { name: "Original", value: cityMetrics.avg_temp },
        { name: "Mitigated", value: cityMetrics.mitigated_temp },
      ]);
      setLoading(false);
    } else {
      // For Custom Location, fallback to default values
      const fallbackMetrics = {
        city: city.value || "Custom Location",
        avg_temp: 35, // default average temp
        mitigated_temp: 32, // default mitigated temp
        level: "Medium",
      };
      setMetrics(fallbackMetrics);
      setChartData([
        { name: "Original", value: fallbackMetrics.avg_temp },
        { name: "Mitigated", value: fallbackMetrics.mitigated_temp },
      ]);
      setLoading(false);
    }

    // Fly to city on the map
    if (mapRef.current) {
      mapRef.current.flyToCity(city);
    }
  };

  return (
    <div className="p-4">
      <CitySearch cities={cities} onChange={handleCityChange} />
      {loading && <p className="mt-4 text-indigo-600">Loading...</p>}
      <Metrics data={metrics} />
      <Graph data={chartData} />
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
