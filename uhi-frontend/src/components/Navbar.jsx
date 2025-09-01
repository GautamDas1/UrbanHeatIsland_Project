import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-indigo-700 text-white px-6 py-4 shadow-md flex justify-between items-center sticky top-0 z-50 font-sans">
      <h1 className="text-xl font-bold">🌍 UHI Visualizer</h1>
      <div className="space-x-4">
        <Link
          to="/"
          className="bg-white text-indigo-700 px-4 py-2 rounded-full hover:bg-indigo-100"
        >
          Home
        </Link>
        <Link
          to="/about"
          className="bg-white text-indigo-700 px-4 py-2 rounded-full hover:bg-indigo-100"
        >
          About
        </Link>
        <Link
          to="/map"
          className="bg-white text-indigo-700 px-4 py-2 rounded-full hover:bg-indigo-100"
        >
          Map
        </Link>
        <Link
          to="/contact"
          className="bg-white text-indigo-700 px-4 py-2 rounded-full hover:bg-indigo-100"
        >
          Contact
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;