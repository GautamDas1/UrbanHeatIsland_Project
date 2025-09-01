// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import About from "./components/About";
import MapPage from "./components/MapPage"; // This now fetches data from backend
import Contact from "./components/Contact";
import "./index.css";
import 'leaflet/dist/leaflet.css';

function App() {
  return (
    <Router>
      <div className="bg-gray-100 min-h-screen text-gray-800">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/map" element={<MapPage />} /> {/* API-driven map */}
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
