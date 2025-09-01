import React, { useEffect, useState } from "react";

const cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Srinagar"];

const cityImages = {
  Delhi: "/images/Delhi.jpg",
  Mumbai: "/images/Mumbai.jpg",
  Chennai: "/images/Chennai.jpg",
  Kolkata: "/images/Kolkata.jpg",
  Bangalore: "/images/Bangalore.jpg",
  Srinagar: "/images/Srinagar.jpg",
};

const About = () => {
  const [temps, setTemps] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTemps = async () => {
      const apiKey = "220ed8731749a0aac8cb99828f4776b6";
      const newTemps = {};

      try {
        for (const city of cities) {
          const res = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`
          );
          if (!res.ok) throw new Error(`Failed to fetch for ${city}`);
          const data = await res.json();
          newTemps[city] =
            data.main && typeof data.main.temp === "number"
              ? data.main.temp
              : null;
        }
        setTemps(newTemps);
        setError(null);
      } catch {
        setError("Failed to fetch temperature data.");
      } finally {
        setLoading(false);
      }
    };
    fetchTemps();
  }, []);

  const getHeatStatus = (temp) => {
    if (temp >= 46) return "Extreme Heat Stress (≥46°C)";
    if (temp >= 38) return "Very Strong Heat (38–46°C)";
    if (temp >= 32) return "Strong Heat Stress (32–38°C)";
    if (temp >= 26) return "Moderate Heat (26–32°C)";
    if (temp >= 9) return "No Thermal Stress (9–26°C)";
    return "Slight Cold Stress (<9°C)";
  };

  const getCardColor = (temp) => {
    if (temp >= 46) return "bg-red-800";
    if (temp >= 38) return "bg-red-600";
    if (temp >= 32) return "bg-orange-500";
    if (temp >= 26) return "bg-yellow-400";
    if (temp >= 9) return "bg-green-500";
    return "bg-blue-400";
  };

  const getCityDescription = (temp) => {
    if (temp === null) return "Unable to fetch temperature data for this city.";
    if (temp >= 46)
      return "Extreme urban heat likely causing severe thermal discomfort.";
    if (temp >= 38)
      return "Very strong heat stress with intensified UHI effects.";
    if (temp >= 32)
      return "Strong heat stress observed. Noticeable urban heat buildup.";
    if (temp >= 26)
      return "Moderate heat, may feel hotter in built-up zones.";
    if (temp >= 9)
      return "Comfortable. UHI effects minimal.";
    return "Cooler with minimal UHI impact.";
  };

  return (
    <div className="relative w-full min-h-screen overflow-hidden">
      {/* Background gradient pattern */}
      <div className="absolute inset-0 bg-gradient-to-br from-rose-100 via-orange-100 to-yellow-100 z-0" />
      {/* Pattern overlay */}
      <div className="absolute inset-0 bg-[url('/images/pattern.svg')] opacity-10 z-0" />

      <div className="relative z-10 max-w-6xl mx-auto py-16 px-4 space-y-12 text-gray-800">
        <h2 className="text-3xl md:text-4xl font-bold text-green-800 text-center">
          About the Project
        </h2>

        <p className="text-gray-700 max-w-3xl mx-auto text-lg text-center">
          This platform analyzes Urban Heat Island (UHI) effects using AI and live weather data.
          It helps citizens, researchers, and urban planners monitor and mitigate UHI in Indian cities.
        </p>

        {/* Key Features */}
        <div className="bg-white/90 p-6 rounded-xl shadow-lg max-w-4xl mx-auto">
          <h3 className="text-2xl font-semibold mb-4 text-green-700">Key Features</h3>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li><strong>Live Temperature Monitoring:</strong> Real-time data for Indian cities.</li>
            <li><strong>UHI Classification:</strong> Heat stress classified by severity.</li>
            <li><strong>Visual Insights:</strong> Map and image-based views (in other sections).</li>
            <li><strong>City-wise UHI Summary:</strong> Explanation of UHI per city with visuals.</li>
            <li><strong>AI-based Forecast (Upcoming):</strong> Land use & green zone prediction system.</li>
            <li><strong>User-Centric Design:</strong> Intuitive and informative layout.</li>
          </ul>
        </div>

        {/* UHI Illustration */}
        <div className="w-full max-w-4xl mx-auto rounded-xl overflow-hidden shadow-md">
          <img
            src="/images/download.jpg"
            alt="UHI Infographic"
            className="w-full h-auto object-contain"
          />
          <p className="text-sm text-gray-600 mt-2 text-center">
            Illustration: Cities absorb and retain more heat than rural areas.
          </p>
        </div>

        {/* Live UHI cards */}
        <div>
          <h3 className="text-2xl font-semibold mb-6 text-green-700 text-center">
            Live UHI Conditions in Indian Cities
          </h3>
          {loading ? (
            <div className="text-center text-lg text-gray-600 py-8">Loading weather data...</div>
          ) : error ? (
            <div className="text-center text-red-600 py-8">{error}</div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {cities.map((city) => {
                const temp = temps[city];
                const heatStatus = temp !== null ? getHeatStatus(temp) : "Unavailable";
                const bgColor = temp !== null ? getCardColor(temp) : "bg-gray-400";
                const description = getCityDescription(temp);

                return (
                  <div
                    key={city}
                    className={`rounded-xl shadow-md overflow-hidden transform hover:scale-105 transition duration-300 ${bgColor} text-white`}
                  >
                    <img
                      src={cityImages[city]}
                      alt={city}
                      className="w-full h-40 object-cover"
                      onError={(e) => (e.target.src = "/images/cities/placeholder.jpg")}
                    />
                    <div className="p-4 text-left space-y-2">
                      <h4 className="text-lg font-bold">{city}</h4>
                      {temp !== null ? (
                        <>
                          <p className="text-sm">Current Temp: {temp.toFixed(1)}°C</p>
                          <p className="text-sm">{heatStatus}</p>
                          <p className="text-xs text-white/90 italic">{description}</p>
                        </>
                      ) : (
                        <p className="text-sm text-gray-200">Weather data unavailable</p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default About;
