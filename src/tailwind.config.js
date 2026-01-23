/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class", // Stitch 원본 설정 반영
  theme: {
    extend: {
      colors: {
        // Stitch 원본에 있던 핵심 유리 색상 추가
        "primary-glass": "rgba(255, 255, 255, 0.15)", 
        "accent-cyan": "#00f2ff",
        "accent-lavender": "#e0b0ff",
        "accent-pink": "#ff7eb3",
      },
      fontFamily: {
        "display": ["Plus Jakarta Sans", "sans-serif"]
      },
      borderRadius: {
        "DEFAULT": "1.5rem",
        "lg": "2rem",
        "xl": "3rem",
        "full": "9999px" // Stitch 원본에 있던 완전 둥글게 설정
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}