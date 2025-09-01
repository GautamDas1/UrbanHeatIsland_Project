// src/api/axios.js
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:5001/api", // Make sure this matches your Flask backend port
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
