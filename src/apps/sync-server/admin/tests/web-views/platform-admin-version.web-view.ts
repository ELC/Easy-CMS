import { expect, type Page } from "@playwright/test";

export class PlatformAdminVersionWebView {
  private constructor(private readonly page: Page) {}

  static async openWithHarReplay(page: Page): Promise<PlatformAdminVersionWebView> {
    await page.routeFromHAR("tests/fixtures/har/sync-server-version.har", {
      update: process.env.PLAYWRIGHT_UPDATE_HAR === "1",
    });
    await page.goto("/");
    return new PlatformAdminVersionWebView(page);
  }

  async expectVersionBadge(version: string): Promise<this> {
    await expect(this.page.getByLabel("Sync Server version")).toContainText(version);
    return this;
  }
}
