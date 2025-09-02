// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import About from "./components/About";
import MapPage from "./components/MapPage";
import Contact from "./components/Contact";
import UHIApp from "./components/UHIApp";
import cities from "./data/cities.json";
import "./index.css";
import "leaflet/dist/leaflet.css";

function App() {
  return (
    <Router>
      <div className="bg-gray-100 min-h-screen text-gray-800">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/uhi" element={<UHIApp cities={cities} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
