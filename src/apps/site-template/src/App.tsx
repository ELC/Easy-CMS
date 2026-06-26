import { VersionBadge } from "design-system";
import { match } from "ts-pattern";

import packageJson from "../package.json";
import "./app.scss";

const generatedSiteWebViewState = {
  ready: "ready",
} as const;

type GeneratedSiteWebViewState = {
  readonly state: typeof generatedSiteWebViewState.ready;
  readonly version: string;
};

function ReadyWebView({ version }: { readonly version: string }) {
  return (
    <main className="generated-site">
      <header className="generated-site__header">
        <h1 className="generated-site__title">Generated Site</h1>
        <VersionBadge label="Generated Site version" version={version} />
      </header>
    </main>
  );
}

export function App() {
  const webViewState: GeneratedSiteWebViewState = {
    state: generatedSiteWebViewState.ready,
    version: packageJson.version,
  };

  return match(webViewState)
    .with({ state: generatedSiteWebViewState.ready }, ({ version }) => (
      <ReadyWebView version={version} />
    ))
    .exhaustive();
}
