// import React, { useEffect, useState } from "react";
// import { Card, CardContent } from "@/components/ui/card";
// import {
//   BarChart,
//   Bar,
//   XAxis,
//   YAxis,
//   Tooltip,
//   Legend,
//   PieChart,
//   Pie,
//   Cell,
//   LineChart,
//   Line,
//   ResponsiveContainer,
// } from "recharts";

// const Dashboard = ({ city }) => {
//   const [metrics, setMetrics] = useState(null);

//   useEffect(() => {
//     if (city) {
//       fetch(
//         `http://127.0.0.1:5000/api/predict?lat=${city.lat}&lon=${city.lon}&city=${city.name}`
//       )
//         .then((res) => res.json())
//         .then((data) => setMetrics(data))
//         .catch((err) => console.error("API fetch error:", err));
//     }
//   }, [city]);

//   if (!metrics) return <p className="text-center mt-10">Loading data...</p>;

//   // ✅ Chart 1: UHI Metrics (fixed version)
//   const uhiData = [
//     { name: "Original Temp (°C)", value: metrics.avg_temp },
//     { name: "Mitigated Temp (°C)", value: metrics.mitigated_temp },
//   ];

//   // ✅ Chart 2: Green Space
//   const greenSpaceData = [
//     { name: "Green Space %", value: metrics.green_space_percent || 0 },
//     {
//       name: "Urban Area %",
//       value: 100 - (metrics.green_space_percent || 0),
//     },
//   ];

//   // ✅ Chart 3: AI vs Satellite
//   // NOTE: We simulate Satellite raw value slightly higher than avg_temp
//   const aiData = [
//     { name: "Satellite LST", value: metrics.avg_temp + 2 },
//     { name: "AI Predicted", value: metrics.avg_temp },
//   ];

//   const COLORS = ["#4ade80", "#f87171"];

//   return (
//     <div className="p-6">
//       {/* AI Badge */}
//       <div className="flex justify-end mb-4">
//         <span className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-xl shadow-lg animate-pulse">
//           🤖 Powered by AI (Linear Regression)
//         </span>
//       </div>

//       {/* Dashboard Grid */}
//       <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
//         {/* Chart 1: UHI Metrics */}
//         <Card className="shadow-xl rounded-2xl">
//           <CardContent>
//             <h2 className="text-lg font-semibold mb-4">UHI Metrics</h2>
//             <ResponsiveContainer width="100%" height={300}>
//               <BarChart data={uhiData}>
//                 <XAxis dataKey="name" />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 <Bar dataKey="value" fill="#6366f1" barSize={60} />
//               </BarChart>
//             </ResponsiveContainer>
//             <p className="mt-2 text-center">
//               UHI Level:{" "}
//               <span className="font-bold text-red-500">{metrics.level}</span>
//             </p>
//           </CardContent>
//         </Card>

//         {/* Chart 2: Green Space */}
//         <Card className="shadow-xl rounded-2xl">
//           <CardContent>
//             <h2 className="text-lg font-semibold mb-4">
//               Green Space Distribution
//             </h2>
//             <ResponsiveContainer width="100%" height={300}>
//               <PieChart>
//                 <Pie
//                   data={greenSpaceData}
//                   dataKey="value"
//                   nameKey="name"
//                   cx="50%"
//                   cy="50%"
//                   outerRadius={100}
//                   label
//                 >
//                   {greenSpaceData.map((entry, index) => (
//                     <Cell
//                       key={`cell-${index}`}
//                       fill={COLORS[index % COLORS.length]}
//                     />
//                   ))}
//                 </Pie>
//                 <Legend />
//               </PieChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>

//         {/* Chart 3: AI Detection */}
//         <Card className="shadow-xl rounded-2xl">
//           <CardContent>
//             <h2 className="text-lg font-semibold mb-4">
//               AI vs Satellite Data
//             </h2>
//             <ResponsiveContainer width="100%" height={300}>
//               <LineChart data={aiData}>
//                 <XAxis dataKey="name" />
//                 <YAxis />
//                 <Tooltip />
//                 <Legend />
//                 <Line
//                   type="monotone"
//                   dataKey="value"
//                   stroke="#10b981"
//                   strokeWidth={3}
//                 />
//               </LineChart>
//             </ResponsiveContainer>
//           </CardContent>
//         </Card>
//       </div>
//     </div>
//   );
// };

// export default Dashboard;
