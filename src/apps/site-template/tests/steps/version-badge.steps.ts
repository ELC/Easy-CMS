import { createBdd } from "playwright-bdd";

import { GeneratedSiteVersionWebView } from "../web-views/generated-site-version.web-view";

const { Given, Then } = createBdd();

let generatedSiteVersionWebView: GeneratedSiteVersionWebView;

Given("the Generated Site version Web View is open", async ({ page }) => {
  generatedSiteVersionWebView = await GeneratedSiteVersionWebView.open(page);
});

Then("the Generated Site version badge shows {string}", async ({ page }, version: string) => {
  void page;
  await generatedSiteVersionWebView.expectVersionBadge(version);
});
