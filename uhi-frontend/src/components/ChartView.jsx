import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const ChartView = ({ data }) => {
  return (
    <div className="bg-white rounded-lg p-4 shadow-md my-4">
      <h2 className="text-xl font-semibold text-center text-gray-700 mb-2">📊 LST Comparison</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="name" />
          <YAxis unit="°C" />
          <Tooltip />
          <Bar dataKey="value" fill="#3182CE" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartView;
