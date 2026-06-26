import { expect, test } from "@playwright/test";

test("renders the Sync Server version badge from the Sync Server version endpoint", async ({ page }) => {
  await page.routeFromHAR("tests/fixtures/har/sync-server-version.har", {
    update: process.env["PLAYWRIGHT_UPDATE_HAR"] === "1",
  });

  await page.goto("/");

  await expect(page.getByLabel("Sync Server version")).toContainText("0.1.0");
});
