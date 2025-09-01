import { useEffect, useState } from "react";
import Select from "react-select";
import axiosInstance from "../api/axios"; // Pre-configured Axios

const CitySearch = ({ onChange }) => {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCities = async () => {
      try {
        const res = await axiosInstance.get("/cities"); // -> http://127.0.0.1:5001/api/cities

        if (!Array.isArray(res.data)) {
          console.warn("Unexpected city data format:", res.data);
          return;
        }

        const cityOptions = res.data
          .map((city) => {
            const lat = parseFloat(city.lat ?? city.coordinates?.lat);
            const lon = parseFloat(city.lon ?? city.coordinates?.lon);

            if (!isNaN(lat) && !isNaN(lon)) {
              return {
                value: { name: city.name, lat, lon },
                label: city.name,
              };
            } else {
              console.warn(`Skipping city "${city.name}" due to invalid coordinates.`, city);
              return null;
            }
          })
          .filter(Boolean);

        setOptions(cityOptions);
      } catch (error) {
        console.error("Error fetching cities:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCities();
  }, []);

  const customStyles = {
    control: (base) => ({
      ...base,
      borderRadius: "0.5rem",
      borderColor: "#d1d5db",
      padding: "0.1rem 0.3rem",
      boxShadow: "none",
      "&:hover": { borderColor: "#6366f1" },
    }),
    menu: (base) => ({ ...base, zIndex: 100 }),
  };

  return (
    <div className="w-full sm:w-1/2 mx-auto">
      <Select
        options={options}
        styles={customStyles}
        placeholder={loading ? "Loading cities..." : "🔍 Search Indian cities..."}
        isLoading={loading}
        onChange={(selected) => onChange?.(selected?.value)}
        className="text-sm"
        isClearable
      />
    </div>
  );
};

export default CitySearch;
