export const importProvenance = {
  archiveFile: "WwFe95NEDEmvPwhe-grok-workspace.zip",
  archiveSha256: "523e2e89cc33abaa1818c68f55b3e6b37e22907a6b4e75e21037bbbf0c1ea5cf",
  sourceWorkspace: "Grok workspace package",
  importedAt: "2026-09-22",
  manifest: {
    name: "app-builder-workspace",
    private: true,
    type: "module",
    scripts: {
      dev: "node scripts/with-app-env.mjs vite dev --host 0.0.0.0 --port 8080",
      build: "node scripts/with-app-env.mjs vite build && npm run db:migrate",
      typecheck: "tsc --noEmit",
      test: "node --test scripts/**/*.test.mjs && node --experimental-strip-types --test src/lib/app-data/app-data.test.ts src/lib/app-data/readiness-schedule.test.ts src/lib/auth/gate-identity.test.ts src/lib/auth/sign-in-gate.test.ts",
    },
    keyDependencies: {
      react: "^19.2.0",
      vite: "^8.2.0",
      recharts: "^2.13.0",
      tanstackRouter: "^1.170.0",
      tailwindcss: "^4.3.0",
    },
  },
} as const;
