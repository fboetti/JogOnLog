import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      usePolling: true,
    },
    hmr: {        // Removes the /ws error in the console
      clientPort: 3000,
    },
    host: true, // needed for the Docker Container port mapping to work
    strictPort: true,
    port: 3000,
  }, 
})
