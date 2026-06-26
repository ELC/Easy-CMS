import { VersionBadge } from "design-system";

import { useReadVersionVersionGet } from "./generated/studioService";

export function App() {
  const versionQuery = useReadVersionVersionGet({
    axios: {
      baseURL: "http://127.0.0.1:8001",
    },
  });

  if (versionQuery.isLoading) {
    return <main>Loading CMS Studio version...</main>;
  }

  if (versionQuery.isError) {
    return <main>CMS Studio version unavailable</main>;
  }

  return (
    <main>
      <h1>CMS Studio</h1>
      <VersionBadge label="CMS Studio version" version={versionQuery.data.data.version} />
    </main>
  );
}
