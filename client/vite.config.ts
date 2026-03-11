import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    // Exclude server files from build
    rollupOptions: {
      external: ['fs', 'path', 'csv-parser']
    }
  },
  // Don't process server files
  optimizeDeps: {
    exclude: ['server']
  }
})
