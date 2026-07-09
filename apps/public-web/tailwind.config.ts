import type { Config } from "tailwindcss";

// Editorial palette — serious crypto news agency. Restrained: near-black ink on
// warm paper, a single deep accent. No neon, no gradients.
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#16181d",
          soft: "#3a3d44",
          muted: "#6b6f78",
        },
        paper: {
          DEFAULT: "#fbfaf7",
          card: "#ffffff",
        },
        line: "#e6e3db",
        accent: {
          DEFAULT: "#8a1c1c", // deep editorial red
          soft: "#b23a3a",
        },
      },
      fontFamily: {
        serif: ["Georgia", "Cambria", "Times New Roman", "serif"],
        sans: [
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica",
          "Arial",
          "sans-serif",
        ],
      },
      maxWidth: {
        prose: "42rem",
        content: "72rem",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

export default config;
