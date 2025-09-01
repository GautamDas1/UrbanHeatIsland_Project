// src/components/Test.jsx (or any component you want to test from)
import React, { useEffect, useState } from "react";
import axios from "../api/axios";

const Test = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios
      .get("/")
      .then((res) => {
        setMessage(res.data);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
        setMessage("Failed to connect to backend.");
      });
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Test API Call</h2>
      <p className="text-gray-700">{message}</p>
    </div>
  );
};

export default Test;
