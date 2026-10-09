import { defineConfig } from "vite";

export default defineConfig({
  server: {
    proxy: {
      "/products": "http://127.0.0.1:8000",
      "/orders": "http://127.0.0.1:8000",
      "/health": "http://127.0.0.1:8000"
    }
  }
});