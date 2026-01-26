import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/main.tsx'),
      name: 'AutoResearcherWebview',
      formats: ['es'],
      fileName: 'webview'
    },
    rollupOptions: {
      external: ['vscode'],
      output: {
        globals: {
          vscode: 'vscode'
        }
      }
    },
    outDir: '../../out/webview',
    emptyOutDir: true,
    sourcemap: true
  },
  base: './',
  define: {
    global: 'globalThis',
  },
})
