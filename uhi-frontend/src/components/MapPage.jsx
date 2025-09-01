import React, { useState, useEffect, useRef } from "react";
import CitySearch from "./CitySearch";
import MapView from "./MapView";
import Metrics from "./Metrics";
import ChartView from "./ChartView";
import axiosInstance from "../api/axios";

const MapPage = () => {
  const [selectedCity, setSelectedCity] = useState(null);
  const [aoi, setAoi] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  const mapRef = useRef(null); // Reference to MapView to call displayHeatmap()

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

    try {
      setLoading(true);
      setMetrics(null);
      setChartData([]);

      // Fetch prediction
      const predictRes = await axiosInstance.get("/predict", {
        params: { lat, lon, city: cityName },
      });

      const predictionData = predictRes.data;
      if (predictionData) {
        setMetrics({
          level: predictionData.level,
          avg: predictionData.avg_temp,
        });
        setChartData([
          { name: "Original", value: predictionData.avg_temp },
          { name: "Mitigated", value: predictionData.mitigated_temp },
        ]);
      }

      // Fetch heatmap
      const heatmapRes = await axiosInstance.get("/heatmap");
      const heatmapPoints = [];
      if (heatmapRes.data?.heatmap) {
        heatmapRes.data.heatmap.forEach((h) => {
          heatmapPoints.push([h.lat, h.lon, 1]);
        });
      }

      // Call MapView's displayHeatmap
      if (mapRef.current && mapRef.current.displayHeatmap) {
        mapRef.current.displayHeatmap(heatmapPoints, [
          {
            uhi_level: predictionData.level,
            average_temperature_celsius: predictionData.avg_temp,
            mitigated_temperature_celsius: predictionData.mitigated_temp,
          },
        ]);
      }
    } catch (error) {
      console.error("Error fetching UHI data:", error);
      alert(
        "Failed to fetch UHI prediction: " +
          (error.response?.data?.error || error.message)
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCity && selectedCity.lat && selectedCity.lon) {
      // Already handled in handleCityChange
    }
  }, [selectedCity]);

  return (
    <div className="max-w-6xl mx-auto px-6 py-20 font-sans">
      <h2 className="text-4xl font-bold text-indigo-700 mb-8 text-center font-serif">
        🔍 Select City & Explore UHI Map
      </h2>

      <div className="mb-8">
        <CitySearch onChange={handleCityChange} />
      </div>

      <h3 className="text-2xl font-semibold mb-6 text-center text-gray-800">
        🗺️ Draw Area of Interest
      </h3>
      <MapView
        ref={mapRef}
        selectedCity={selectedCity}
        onDraw={handleDraw}
        setMetrics={setMetrics}
        setChartData={setChartData}
        setLoading={setLoading}
      />

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
