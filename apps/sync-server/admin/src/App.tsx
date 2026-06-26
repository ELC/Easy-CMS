import { VersionBadge } from "design-system";

import { useReadVersionVersionGet } from "./generated/syncServerService";

export function App() {
  const versionQuery = useReadVersionVersionGet({
    axios: {
      baseURL: "http://127.0.0.1:8000",
    },
  });

  if (versionQuery.isLoading) {
    return <main>Loading Sync Server version...</main>;
  }

  if (versionQuery.isError) {
    return <main>Sync Server version unavailable</main>;
  }

  return (
    <main>
      <h1>Platform Admin Panel</h1>
      <VersionBadge label="Sync Server version" version={versionQuery.data.data.version} />
    </main>
  );
}
