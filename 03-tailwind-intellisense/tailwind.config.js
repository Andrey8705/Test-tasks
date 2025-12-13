/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./examples/**/*.{html,js,jsx}'],
  theme: {
    extend: {
      colors: {
        'custom-blue': '#1e40af',
        'custom-purple': '#7c3aed',
        'custom-green': '#10b981',
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
      },
      fontSize: {
        '2xs': '0.625rem',
      },
    },
  },
  plugins: [],
};
