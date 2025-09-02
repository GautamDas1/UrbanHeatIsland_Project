import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const ChartView = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="mt-12 p-6 bg-white shadow-lg rounded-xl">
      <h3 className="text-2xl font-bold text-indigo-700 mb-6 text-center">
        📊 Temperature Comparison
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis label={{ value: "°C", angle: -90, position: "insideLeft" }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="value" fill="#4f46e5" barSize={60} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartView;
