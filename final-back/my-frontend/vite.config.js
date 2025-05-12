import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
   server: {
    host: '0.0.0.0', // Важно! Это позволяет подключаться снаружи.
    port: 5173, // Порт, который вы используете
  },
  plugins: [vue()],
})
