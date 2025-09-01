// uhi-backend/routes/uhi.js

const express = require("express");
const axios = require("axios");
const router = express.Router();

// GET /api/uhi/:city - fetches UHI prediction from Flask backend
router.get("/:city", async (req, res) => {
  const city = req.params.city;

  try {
    const response = await axios.get(`http://localhost:5000/api/uhi/${city}`);
    res.json(response.data);
  } catch (error) {
    console.error("Flask UHI fetch failed:", error.message);
    res.status(500).json({ error: "Failed to get UHI data" });
  }
});

module.exports = router;
