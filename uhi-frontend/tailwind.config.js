/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        serif: ['Lora', 'Georgia', 'serif'],
      },
      colors: {
        primary: {
          light: '#c7d2fe',
          DEFAULT: '#6366f1',
          dark: '#4f46e5',
        },
        accent: '#facc15', // optional highlight color
      },
    },
  },
  plugins: [],
};
