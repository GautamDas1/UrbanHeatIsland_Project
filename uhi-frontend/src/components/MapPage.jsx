import React, { useState, useRef, useEffect } from "react";
import CitySearch from "./citySearch";
import MapView from "./MapView";
import Metrics from "./Metrics";
import ChartView from "./ChartView";

const API_BASE = "http://127.0.0.1:5000/api";

const MapPage = () => {
  const [selectedCity, setSelectedCity] = useState(null);
  const [aoi, setAoi] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [cities, setCities] = useState([]);

  const mapRef = useRef(null);

  // 🔹 Load cities from backend
  useEffect(() => {
    fetch(`${API_BASE}/cities`)
      .then((res) => res.json())
      .then((data) => setCities(data))
      .catch((err) => console.error("Error loading cities:", err));
  }, []);

  const handleCityChange = (city) => {
    setSelectedCity(city);
    setAoi(null);
    if (city) {
      handleSubmit(city.lat, city.lon, city.name);
    }
  };

  const handleDraw = (coords) => {
    setAoi(coords);
    setSelectedCity(null);
    if (coords) {
      handleSubmit(coords.lat, coords.lon, "Drawn Area");
    }
  };

  const handleSubmit = async (lat, lon, cityName = "Custom Location") => {
    if (!lat || !lon) {
      alert("Invalid coordinates for analysis.");
      return;
    }

    setLoading(true);
    setMetrics(null);
    setChartData([]);

    try {
      // 🔹 Fetch prediction from backend
      const predictionRes = await fetch(
        `${API_BASE}/predict?lat=${lat}&lon=${lon}&city=${cityName}`
      );
      const predictionData = await predictionRes.json();

      if (predictionData.error) {
        alert(predictionData.error);
        setLoading(false);
        return;
      }

      setMetrics({
        level: predictionData.level,
        avg: predictionData.avg_temp,
      });

      setChartData([
        { name: "Original", value: predictionData.avg_temp },
        { name: "Mitigated", value: predictionData.mitigated_temp },
      ]);

      // 🔹 Fetch heatmap data
      const heatmapRes = await fetch(`${API_BASE}/heatmap`);
      const heatmapJson = await heatmapRes.json();

      const heatmapPoints = heatmapJson.heatmap.map((h) => [
        h.lat,
        h.lon,
        h.intensity,
      ]);

      if (mapRef.current && mapRef.current.displayHeatmap) {
        mapRef.current.displayHeatmap(heatmapPoints, predictionData);
      }
    } catch (err) {
      console.error("Error fetching UHI data:", err);
      alert("Failed to load analysis data.");
    }

    setLoading(false);
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-20 font-sans">
      <h2 className="text-4xl font-bold text-indigo-700 mb-8 text-center font-serif">
        🔍 Select City & Explore UHI Map
      </h2>

      <div className="mb-8">
        <CitySearch cities={cities} onChange={handleCityChange} />
      </div>

      <h3 className="text-2xl font-semibold mb-6 text-center text-gray-800">
        🗺️ Draw Area of Interest
      </h3>
      <MapView ref={mapRef} selectedCity={selectedCity} onDraw={handleDraw} />

      <div className="text-center mt-10">
        <button
          onClick={() => {
            if (selectedCity) {
              handleSubmit(selectedCity.lat, selectedCity.lon, selectedCity.name);
            } else if (aoi) {
              handleSubmit(aoi.lat, aoi.lon, "Drawn Area");
            } else {
              alert("Please select a city or draw an area first to analyze.");
            }
          }}
          disabled={loading}
          className={`${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-gradient-to-r from-indigo-500 to-blue-500 hover:from-indigo-600 hover:to-blue-600"
          } text-white font-bold py-3 px-10 rounded-full shadow-lg hover:shadow-xl transition-all duration-300`}
        >
          {loading ? "Processing..." : "🚀 Submit UHI Analysis"}
        </button>
      </div>

      {metrics && <Metrics data={metrics} />}
      {chartData.length > 0 && <ChartView data={chartData} />}
    </div>
  );
};

export default MapPage;
