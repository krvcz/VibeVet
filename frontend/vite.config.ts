import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    hmr: {
      overlay: false // Disable HMR overlay to prevent module invalidation issues
    }
  },
  // Clear module cache on hot updates
  clearScreen: false,
  // Force clean build cache
  build: {
    emptyOutDir: true
  }
});