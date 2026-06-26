import { createBdd } from "playwright-bdd";

import { StudioVersionWebView } from "../web-views/studio-version.web-view";

const { Given, Then } = createBdd();

let studioVersionWebView: StudioVersionWebView;

Given("the CMS Studio version Web View is open with HAR replay", async ({ page }) => {
  studioVersionWebView = await StudioVersionWebView.openWithHarReplay(page);
});

Then("the CMS Studio version badge shows {string}", async ({ page }, version: string) => {
  void page;
  await studioVersionWebView.expectVersionBadge(version);
});
