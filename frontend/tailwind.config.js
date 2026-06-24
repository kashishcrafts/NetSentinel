export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        cyber: {
          900: "#020617",
          800: "#071319",
          700: "#0f1e2a",
          600: "#19293e",
          500: "#224361",
          400: "#38bdf8",
          300: "#60a5fa"
        }
      },
      boxShadow: {
        glow: "0 0 35px rgba(56, 189, 248, 0.18)"
      }
    }
  },
  plugins: []
};
