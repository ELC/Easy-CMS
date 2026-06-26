import { expect, test } from "@playwright/test";

test("renders the Generated Site CalVer badge", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByLabel("Generated Site version")).toContainText("2026.06.0");
});
