// src/components/Test.jsx
import React, { useEffect, useState } from "react";
import axios from "../api/axios";

const Test = () => {
  const [message, setMessage] = useState("Connecting...");
  const [status, setStatus] = useState("pending"); // "pending", "success", "error"

  useEffect(() => {
    axios
      .get("/") // ✅ Calls backend root route (http://127.0.0.1:5000/)
      .then((res) => {
        const msg =
          res.data?.message || "✅ Backend Connected!";
        setMessage(msg);
        setStatus("success");
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setMessage("❌ Failed to connect to backend.");
        setStatus("error");
      });
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md text-center">
      <h2 className="text-xl font-bold mb-4">🔌 Backend Connection Test</h2>
      <p
        className={`text-lg font-semibold ${
          status === "success"
            ? "text-green-600"
            : status === "error"
            ? "text-red-600"
            : "text-gray-600"
        }`}
      >
        {message}
      </p>
    </div>
  );
};

export default Test;
