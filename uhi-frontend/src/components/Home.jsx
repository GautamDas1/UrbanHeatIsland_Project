import React from "react";
import { Search } from "lucide-react";
import { Link } from "react-router-dom";

const Home = () => {
  const features = [
    ["AI-Powered Predictions", "Analyze temperature patterns using ML"],
    ["Satellite Data", "Real-time remote sensing integration"],
    ["Green Space Planner", "Optimize vegetation for cooling"],
    ["Interactive Maps", "Visualize UHI zones and heat index"]
  ];

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-yellow-50 via-orange-100 to-rose-50 text-gray-800 px-6 py-10 space-y-16">

      {/* Hero Section */}
      <section className="text-center space-y-6 fade-in">
        <h1 className="text-4xl md:text-5xl font-extrabold text-green-700">
          Predict and Mitigate Urban Heat Islands
        </h1>
        <p className="text-lg text-gray-600 max-w-xl mx-auto">
          Using satellite data and AI for sustainable urban planning and heat mitigation.
        </p>
        <Link to="/map">
          <button className="bg-green-600 text-white px-6 py-2 rounded-xl shadow hover:bg-green-700 transition">
            Explore Map
          </button>
        </Link>
      </section>

      {/* Search Bar */}
      <section className="flex justify-center">
        <div className="flex items-center border rounded-full shadow-md px-4 py-2 bg-white w-full max-w-md">
          <Search className="text-gray-500 mr-2" />
          <input
            type="text"
            placeholder="Search for a city..."
            className="w-full outline-none bg-transparent"
          />
        </div>
      </section>

      {/* Overview Section */}
      <section className="max-w-4xl mx-auto text-center space-y-4 bg-white/70 p-6 rounded-xl shadow-md fade-in">
        <h2 className="text-2xl font-semibold text-gray-800">About the Project</h2>
        <p className="text-gray-600">
          Our platform leverages machine learning and satellite imagery to analyze Urban Heat Island (UHI) patterns. The goal is to support city planners, researchers, and citizens in understanding and mitigating heat risks.
        </p>
      </section>

      {/* Feature Cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto fade-in">
        {features.map(([title, desc]) => (
          <div
            key={title}
            className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition card-hover"
          >
            <h3 className="text-lg font-bold text-green-700">{title}</h3>
            <p className="text-sm text-gray-600 mt-2">{desc}</p>
          </div>
        ))}
      </section>

      {/* Map Preview Image Section */}
      <section className="text-center px-4 fade-in">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Heat Map Preview</h2>
        <div className="w-full max-w-5xl mx-auto overflow-hidden rounded-xl shadow-lg border">
          <img
            src="/images/image1.png"
            alt="Universal Thermal Climate Index Map"
            className="w-full h-auto object-contain"
          />
        </div>
        <p className="mt-2 text-sm text-gray-600">
          Above is a sample heat map visualizing the Universal Thermal Climate Index (UTCI) across various Indian cities. This map helps in understanding the urban heat distribution and planning for mitigation strategies.
        </p>
      </section>

      {/* Climate Fact */}
      <section className="text-center max-w-3xl mx-auto mt-10 fade-in">
        <blockquote className="italic text-gray-700 border-l-4 border-green-600 pl-4">
          “Urban areas can be up to 7°C warmer than surrounding rural areas due to the Urban Heat Island effect.”
        </blockquote>
      </section>

    </div>
  );
};

export default Home;
