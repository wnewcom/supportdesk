import vue from "@vitejs/plugin-vue";
import frappeui from "frappe-ui/vite";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    frappeui({
      frappeProxy: true,
      jinjaBootData: true,
      buildConfig: {
        outDir: `../public/desk`,
        emptyOutDir: true,
        indexHtmlPath: "../supportdesk/www/supportdesk/index.html",
      },
    }),
    vue(),
  ],
  server: {
    allowedHosts: true,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      "tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
    },
  },
  optimizeDeps: {
    exclude: ["frappe-ui"],
  },
});
