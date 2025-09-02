// src/components/Graph.jsx
import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const Graph = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="mt-6 p-4 bg-white shadow-lg rounded-xl">
      <h3 className="text-xl font-bold text-indigo-700 mb-2 text-center">🌡️ Temperature Comparison</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#4f46e5" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Graph;
