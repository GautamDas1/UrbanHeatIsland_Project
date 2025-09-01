const express = require("express");
const router = express.Router();
const CityData = require("../models/CityData");

// POST: Add new city data
router.post("/", async (req, res) => {
  try {
    const { name, temperature, description } = req.body;
    const newData = new CityData({ name, temperature, description });
    await newData.save();
    res.status(201).json(newData);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// GET: All city data
router.get("/", async (req, res) => {
  try {
    const data = await CityData.find().sort({ timestamp: -1 });
    res.json(data);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
