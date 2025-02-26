/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        maroon: '#8c003b',
        green: '#006938',
        yellow: '#ffc712',
      },
    },
  },
  plugins: [require('tailwindcss-primeui')]
}