const express = require("express");
const router = express.Router();
const Feedback = require("../models/Feedback");

// POST feedback
router.post("/", async (req, res) => {
  try {
    const newFeedback = new Feedback(req.body);
    await newFeedback.save();
    res.status(201).json({ message: "Feedback received!" });
  } catch (err) {
    res.status(500).json({ error: "Failed to save feedback" });
  }
});

module.exports = router;
