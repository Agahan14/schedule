/** @type {import("tailwindcss").Config} */
module.exports = {
    mode: "jit",
    content: [
        "./src/project/templates/**/*.{html,htm}",
        "./src/project/static/scripts/**/*.{js,ts}",
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        extend: {

            borderWidth: {
                "0.5": "0.5px"  // Custom border width
            }


        }
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/container-queries"),
        require("flowbite/plugin")
    ]
};
