import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  const baseStyle =
    "px-4 py-2 rounded-full font-medium transition-all duration-300";
  const activeStyle =
    "bg-yellow-300 text-indigo-900 shadow-md"; // highlight for active page
  const inactiveStyle =
    "bg-white text-indigo-700 hover:bg-indigo-100 hover:shadow";

  return (
    <nav className="bg-gradient-to-r from-indigo-700 to-indigo-900 text-white px-6 py-4 shadow-md flex justify-between items-center sticky top-0 z-50 font-sans">
      <h1 className="text-xl font-bold tracking-wide">🌍 Urban AI</h1>
      <div className="space-x-3">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `${baseStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          Home
        </NavLink>
        <NavLink
          to="/about"
          className={({ isActive }) =>
            `${baseStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          About
        </NavLink>
        <NavLink
          to="/map"
          className={({ isActive }) =>
            `${baseStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          Map
        </NavLink>
        <NavLink
          to="/contact"
          className={({ isActive }) =>
            `${baseStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          Contact
        </NavLink>
      </div>
    </nav>
  );
};

export default Navbar;
