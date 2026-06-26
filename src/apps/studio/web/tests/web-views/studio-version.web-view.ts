import { expect, type Page } from "@playwright/test";

export class StudioVersionWebView {
  private constructor(private readonly page: Page) {}

  static async openWithHarReplay(page: Page): Promise<StudioVersionWebView> {
    await page.routeFromHAR("tests/fixtures/har/studio-version.har", {
      update: process.env.PLAYWRIGHT_UPDATE_HAR === "1",
    });
    await page.goto("/");
    return new StudioVersionWebView(page);
  }

  async expectVersionBadge(version: string): Promise<this> {
    await expect(this.page.getByLabel("CMS Studio version")).toContainText(version);
    return this;
  }
}
