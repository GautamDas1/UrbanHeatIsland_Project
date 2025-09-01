const mongoose = require("mongoose");

const cityDataSchema = new mongoose.Schema({
  name: { type: String, required: true },
  temperature: { type: Number, required: true },
  description: { type: String },
  timestamp: { type: Date, default: Date.now },
});

module.exports = mongoose.model("CityData", cityDataSchema);
