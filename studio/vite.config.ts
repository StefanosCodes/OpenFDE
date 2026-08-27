import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

const nexusTarget = process.env.NEXUS_API_URL ?? "http://127.0.0.1:8000";
const nexusServiceKey = process.env.NEXUS_API_KEY ?? "openfde-local-dev-key";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/api/nexus": {
        target: nexusTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/nexus/, ""),
        configure: (proxy) => {
          proxy.on("proxyReq", (proxyRequest) => {
            proxyRequest.setHeader("Authorization", `Bearer ${nexusServiceKey}`);
          });
        },
      },
    },
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"],
    setupFiles: ["./src/test/setup.ts"],
    restoreMocks: true,
  },
});
