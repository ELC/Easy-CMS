import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  use: {
    baseURL: "http://127.0.0.1:4175",
    ...devices["Desktop Chrome"],
  },
  webServer: {
    command: "pnpm dev --port 4175",
    reuseExistingServer: true,
    url: "http://127.0.0.1:4175",
  },
});
