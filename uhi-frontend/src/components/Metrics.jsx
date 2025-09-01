import React from "react";

const Metrics = ({ data }) => {
  return (
    <div className="bg-white rounded-lg p-4 shadow-md my-4 text-center">
      <h2 className="text-xl font-semibold text-gray-700 mb-2">🔥 UHI Metrics</h2>
      <p className="text-lg">UHI Risk Level: <strong>{data.level}</strong></p>
      <p className="text-lg">Avg LST: <strong>{data.avg}°C</strong></p>
    </div>
  );
};

export default Metrics;
