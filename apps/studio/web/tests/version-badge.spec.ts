import { expect, test } from "@playwright/test";

test("renders the CMS Studio version badge from the sidecar version endpoint", async ({ page }) => {
  await page.routeFromHAR("tests/fixtures/har/studio-version.har", {
    update: process.env["PLAYWRIGHT_UPDATE_HAR"] === "1",
  });

  await page.goto("/");

  await expect(page.getByLabel("CMS Studio version")).toContainText("0.1.0");
});
