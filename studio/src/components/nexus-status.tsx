import { useEffect, useState } from "react";

import { getNexusHealth, listAccounts } from "../api/nexus";

type ConnectionState =
  | { kind: "loading" }
  | { kind: "ready"; accountCount: number | null }
  | { kind: "error"; message: string };

export function NexusStatus() {
  const [connection, setConnection] = useState<ConnectionState>({ kind: "loading" });

  useEffect(() => {
    const controller = new AbortController();

    async function connect() {
      try {
        const health = await getNexusHealth(controller.signal);
        if (health.status !== "ready") {
          throw new Error("Nexus is not ready.");
        }
        if (import.meta.env.DEV) {
          const accounts = await listAccounts(controller.signal);
          setConnection({ kind: "ready", accountCount: accounts.items.length });
        } else {
          setConnection({ kind: "ready", accountCount: null });
        }
      } catch (error) {
        if (controller.signal.aborted) {
          return;
        }
        setConnection({
          kind: "error",
          message: error instanceof Error ? error.message : "Nexus is unavailable.",
        });
      }
    }

    void connect();
    return () => controller.abort();
  }, []);

  if (connection.kind === "loading") {
    return (
      <div className="nexus-status" role="status">
        <span className="status-dot status-loading" />
        Checking Nexus
      </div>
    );
  }

  if (connection.kind === "error") {
    return (
      <div className="nexus-status nexus-error" role="status" title={connection.message}>
        <span className="status-dot status-error" />
        Nexus unavailable
      </div>
    );
  }

  return (
    <div className="nexus-status" role="status">
      <span className="status-dot status-ready" />
      Nexus ready
      {connection.accountCount === null ? null : (
        <span className="diagnostic-count"> · {connection.accountCount} accounts reachable</span>
      )}
    </div>
  );
}
