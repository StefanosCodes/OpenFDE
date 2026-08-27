import { defineConfig, globalIgnores } from "eslint/config";
import tseslint from "typescript-eslint";

export default defineConfig([
  globalIgnores([
    ".next/**",
    "dist/**",
    "coverage/**",
    "playwright-report/**",
    "src/api/nexus.generated.ts",
  ]),
  ...tseslint.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],
    rules: {
      "@typescript-eslint/consistent-type-imports": "error",
    },
  },
]);
