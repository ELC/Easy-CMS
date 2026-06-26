import { defineConfig } from "orval";

export default defineConfig({
  studioService: {
    input: "../service/openapi.json",
    output: {
      target: "src/generated/studioService.ts",
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
