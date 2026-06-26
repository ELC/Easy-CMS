import { VersionBadge } from "design-system";
import { match } from "ts-pattern";

import { useReadVersionVersionGet } from "./generated/syncServerService";
import "./app.scss";

const platformAdminWebViewState = {
  loading: "loading",
  unavailable: "unavailable",
  ready: "ready",
} as const;

type PlatformAdminWebViewState =
  | { readonly state: typeof platformAdminWebViewState.loading }
  | { readonly state: typeof platformAdminWebViewState.unavailable }
  | { readonly state: typeof platformAdminWebViewState.ready; readonly version: string };

function LoadingWebView() {
  return <main className="platform-admin">Loading Sync Server version...</main>;
}

function UnavailableWebView() {
  return <main className="platform-admin">Sync Server version unavailable</main>;
}

function ReadyWebView({ version }: { readonly version: string }) {
  return (
    <main className="platform-admin">
      <header className="platform-admin__header">
        <h1 className="platform-admin__title">Platform Admin Panel</h1>
        <VersionBadge label="Sync Server version" version={version} />
      </header>
    </main>
  );
}

export function App() {
  const versionQuery = useReadVersionVersionGet({
    axios: {
      baseURL: "http://127.0.0.1:8000",
    },
  });

  const webViewState: PlatformAdminWebViewState = versionQuery.isLoading
    ? { state: platformAdminWebViewState.loading }
    : versionQuery.isError || versionQuery.data === undefined
      ? { state: platformAdminWebViewState.unavailable }
      : { state: platformAdminWebViewState.ready, version: versionQuery.data.data.version };

  return match(webViewState)
    .with({ state: platformAdminWebViewState.loading }, () => <LoadingWebView />)
    .with({ state: platformAdminWebViewState.unavailable }, () => <UnavailableWebView />)
    .with({ state: platformAdminWebViewState.ready }, ({ version }) => (
      <ReadyWebView version={version} />
    ))
    .exhaustive();
}
