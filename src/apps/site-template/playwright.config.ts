import { defineConfig, devices } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const testDir = defineBddConfig({
  features: "tests/features/*.feature",
  steps: "tests/steps/*.ts",
});

export default defineConfig({
  testDir,
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
