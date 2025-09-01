// server.js

const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 4000; // Change to 4000 if Flask uses 5000

// Middleware
app.use(cors());
app.use(express.json());

// Routes
const feedbackRoutes = require("./routes/feedback");
const cityRoutes = require("./routes/cities");
const uhiRoutes = require("./routes/uhi"); // <-- NEW LINE

app.use("/api/feedback", feedbackRoutes);
app.use("/api/cities", cityRoutes);
app.use("/api/uhi", uhiRoutes); // <-- NEW LINE

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log("✅ MongoDB connected"))
  .catch((err) => console.error("❌ MongoDB connection error:", err));

// Root route (optional)
app.get("/", (req, res) => {
  res.send("🌍 UHI Node Backend is running!");
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Node backend is running on http://localhost:${PORT}`);
});
