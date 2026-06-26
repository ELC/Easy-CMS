import { defineConfig } from "orval";

export default defineConfig({
  syncServerService: {
    input: "../service/openapi.json",
    output: {
      target: "src/generated/syncServerService.ts",
      client: "react-query",
      httpClient: "axios",
      mode: "single",
      mock: false,
      override: {
        query: {
          useQuery: true,
        },
      },
    },
  },
});
