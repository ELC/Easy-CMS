import { createBdd } from "playwright-bdd";

import { PlatformAdminVersionWebView } from "../web-views/platform-admin-version.web-view";

const { Given, Then } = createBdd();

let platformAdminVersionWebView: PlatformAdminVersionWebView;

Given("the Platform Admin Panel version Web View is open with HAR replay", async ({ page }) => {
  platformAdminVersionWebView = await PlatformAdminVersionWebView.openWithHarReplay(page);
});

Then("the Sync Server version badge shows {string}", async ({ page }, version: string) => {
  void page;
  await platformAdminVersionWebView.expectVersionBadge(version);
});
