import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  
  // CRITICAL FIX: Set base to '/' for proper routing on deployed site
  base: '/',
  
  // Build configuration
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
  },
  
  // Server configuration for development
  server: {
    port: 5173,
    strictPort: false,
    host: true,
  },
  
  // Preview configuration
  preview: {
    port: 4173,
    strictPort: false,
    host: true,
  }
})