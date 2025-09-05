import React from "react";
import Select from "react-select";

const CitySearch = ({ cities, onChange }) => {
  const options = cities.map((city) => ({
    value: city.name,
    label: city.name,
    lat: city.lat,
    lon: city.lon,
  }));

  // Add a Custom Location option at the end
  const customOption = {
    value: "Custom Location",
    label: "📍 Custom Location (draw on map)",
    lat: null,
    lon: null,
  };

  return (
    <Select
      options={[...options, customOption]}
      onChange={(opt) => {
        // Pass the selected city to parent
        onChange({
          city: opt.value,
          lat: opt.lat,
          lon: opt.lon,
        });
      }}
      placeholder="🔍 Search for a city..."
      className="w-full text-sm"
      styles={{
        control: (base) => ({
          ...base,
          borderRadius: "0.5rem",
          borderColor: "#d1d5db", // Tailwind gray-300
          boxShadow: "none",
          "&:hover": { borderColor: "#9ca3af" }, // Tailwind gray-400
        }),
      }}
    />
  );
};

export default CitySearch;
