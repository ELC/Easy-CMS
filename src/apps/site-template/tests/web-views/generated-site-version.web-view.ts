import { expect, type Page } from "@playwright/test";

export class GeneratedSiteVersionWebView {
  private constructor(private readonly page: Page) {}

  static async open(page: Page): Promise<GeneratedSiteVersionWebView> {
    await page.goto("/");
    return new GeneratedSiteVersionWebView(page);
  }

  async expectVersionBadge(version: string): Promise<this> {
    await expect(this.page.getByLabel("Generated Site version")).toContainText(version);
    return this;
  }
}
