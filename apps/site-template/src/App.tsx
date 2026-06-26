import { VersionBadge } from "design-system";

import packageJson from "../package.json";

export function App() {
  return (
    <main>
      <h1>Generated Site</h1>
      <VersionBadge label="Generated Site version" version={packageJson.version} />
    </main>
  );
}
