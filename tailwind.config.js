/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: [
    "./src/project/templates/**/*.{html,htm}",
    "./src/project/static/scripts/**/*.{js,ts}",
  ],
  theme: {
    extend: {

     
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/container-queries"),
  ],
};
