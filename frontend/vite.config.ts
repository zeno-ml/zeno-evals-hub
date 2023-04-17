import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: "../zeno-evals-hub/frontend/build",
    manifest: true,
    target: "esnext",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: "src/main.ts",
      },
    },
  },
});
