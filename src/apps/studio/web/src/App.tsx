import { VersionBadge } from "design-system";
import { match } from "ts-pattern";

import { useReadVersionVersionGet } from "./generated/studioService";
import "./app.scss";

const studioWebViewState = {
  loading: "loading",
  unavailable: "unavailable",
  ready: "ready",
} as const;

type StudioWebViewState =
  | { readonly state: typeof studioWebViewState.loading }
  | { readonly state: typeof studioWebViewState.unavailable }
  | { readonly state: typeof studioWebViewState.ready; readonly version: string };

function LoadingWebView() {
  return <main className="cms-studio">Loading CMS Studio version...</main>;
}

function UnavailableWebView() {
  return <main className="cms-studio">CMS Studio version unavailable</main>;
}

function ReadyWebView({ version }: { readonly version: string }) {
  return (
    <main className="cms-studio">
      <header className="cms-studio__header">
        <h1 className="cms-studio__title">CMS Studio</h1>
        <VersionBadge label="CMS Studio version" version={version} />
      </header>
    </main>
  );
}

export function App() {
  const versionQuery = useReadVersionVersionGet({
    axios: {
      baseURL: "http://127.0.0.1:8001",
    },
  });

  const webViewState: StudioWebViewState = versionQuery.isLoading
    ? { state: studioWebViewState.loading }
    : versionQuery.isError || versionQuery.data === undefined
      ? { state: studioWebViewState.unavailable }
      : { state: studioWebViewState.ready, version: versionQuery.data.data.version };

  return match(webViewState)
    .with({ state: studioWebViewState.loading }, () => <LoadingWebView />)
    .with({ state: studioWebViewState.unavailable }, () => <UnavailableWebView />)
    .with({ state: studioWebViewState.ready }, ({ version }) => <ReadyWebView version={version} />)
    .exhaustive();
}
