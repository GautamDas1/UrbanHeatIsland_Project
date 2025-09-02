// src/components/Metrics.jsx
import React from "react";

const Metrics = ({ data }) => {
  if (!data) return null;

  return (
    <div className="mt-6 p-6 bg-white shadow-lg rounded-xl text-center">
      <h3 className="text-2xl font-bold text-indigo-700 mb-4">🌡️ UHI Metrics</h3>
      <p className="text-lg text-gray-800">
        <strong>City:</strong> {data.city || "Custom Location"}
      </p>
      <p className="text-lg text-gray-800">
        <strong>UHI Level:</strong>{" "}
        <span
          className={
            data.level === "High"
              ? "text-red-600 font-semibold"
              : data.level === "Medium"
              ? "text-yellow-600 font-semibold"
              : "text-green-600 font-semibold"
          }
        >
          {data.level}
        </span>
      </p>
      <p className="text-lg text-gray-800">
        <strong>Average Temp:</strong> {data.avg_temp} °C
      </p>
      <p className="text-lg text-gray-800">
        <strong>Mitigated Temp:</strong> {data.mitigated_temp} °C
      </p>
    </div>
  );
};

export default Metrics;
