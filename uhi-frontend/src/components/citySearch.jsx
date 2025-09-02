import React from "react";
import Select from "react-select";

const CitySearch = ({ cities, onChange }) => {
  const options = cities.map((city) => ({
    value: city.name,
    label: city.name,
    lat: city.lat,
    lon: city.lon,
  }));

  // Add a Custom Location option
  const customOption = { value: "Custom Location", label: "Custom Location", lat: null, lon: null };

  return (
    <Select
      options={[...options, customOption]}
      onChange={(opt) => {
        // If user selects Custom Location, pass placeholder lat/lon (or null) to parent
        if (opt.value === "Custom Location") {
          onChange({
            city: opt.value,
            lat: opt.lat,
            lon: opt.lon,
          });
        } else {
          onChange({
            city: opt.value,
            lat: opt.lat,
            lon: opt.lon,
          });
        }
      }}
      placeholder="Search for a city..."
      className="w-full"
    />
  );
};

export default CitySearch;
