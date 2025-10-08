import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        port: 8080,
        host: true
    },
    preview: {
        port: 8080,
        host: true
    },
    define: {
        __BACKEND_URL__: JSON.stringify(process.env.BACKEND_URL || 'http://localhost:8000')
    }
})